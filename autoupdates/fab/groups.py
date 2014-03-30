# -*- coding: utf8 -*-

""" Automatic updating tables regarding VK groups """

from base import Updater, Progress
from datetime import datetime
from fabric.api import env
from multiprocessing import Process

import fabric.api
import fabric.context_managers
import os
import settings


class GroupsUpdater(Updater):

    def __init__(self, tracker):

        super(GroupsUpdater, self).__init__(tracker)

        self.is_local = settings.UPDATING_GROUPS_HOST == ''
        self.timestamp = self._get_timestamp()
        self.outfile = './data/groups_output_' + self.timestamp + '.csv'
        self.basic_log_filename = 'groups_{0}_output.log'.format(self.timestamp)
        self.error_log_filename = 'groups_{0}_error.log'.format(self.timestamp)

        self.is_debug = settings.DEBUG

        self._set_up_env()

    def _delete_file(self, filename, is_local=True):
        if is_local is True:
            func = fabric.api.local
        else:
            func = fabric.api.run

        with fabric.context_managers.settings(warn_only=True):
            func('unlink {0}'.format(filename))

    def _cleanup(self):

        if self.is_local is False:
            self._delete_file(self.basic_log_filename, False)
            self._delete_file(self.error_log_filename, False)
            self._delete_file(self.outfile, False)
            self._delete_file(self.outfile + '.gz', False)

        self._delete_file(self.outfile)

    def _get_timestamp(self):
        now = datetime.now()
        # dd-mm-yyyy_hh-mm
        return now.strftime("%d-%m-%Y_%H-%M")

    def _get_vk_groups_count(self):
        command = 'python ./autoupdates/collectors/groups.py groups_count'
        response = fabric.api.run(command, quiet=True)
        return int(response)

    def _set_up_env(self):
        if not self.is_local:
            env.host_string = settings.UPDATING_GROUPS_HOST

            user = settings.UPDATING_GROUPS_USER
            if user.find(':') >= 0:
                env.user, env.password = user.split(':')
            else:
                env.user = user

    def _import_data(self):
        self.tracker.step("Importing data...")

        fabric.api.local('chmod 644 {0}'.format(self.outfile))
        fabric.api.local('./manage.py import_groups {0}'.format(
            os.path.join(os.getcwd(), self.outfile)
        ))

    def _put_executables(self):
        self.tracker.step("Putting the executable file into remote host...")

        fabric.api.run('mkdir -p autoupdates/collectors')
        with fabric.api.lcd('autoupdates/collectors/'):
            fabric.api.put('*.py', './autoupdates/collectors/')

    def _remote_run(self):
        command = 'nohup python ./autoupdates/collectors/groups.py --from 1 --to {0} --output {1} --min-people {2} collect'.format(
            self.groups_count,
            self.outfile,
            settings.UPDATING_GROUPS_MIN_PEOPLE
        )
        command = command + ' > {0} 2> {1} < /dev/null &'.format(
            self.basic_log_filename,
            self.error_log_filename
        )
        fabric.api.run(command, pty=False)

    def _local_run(self):

        def run_worker():
            command = 'python ./autoupdates/collectors/groups.py --from 1 --to {0} --output {1} --min-people {2} collect'.format(
                self.groups_count,
                self.outfile,
                settings.UPDATING_GROUPS_MIN_PEOPLE
            )
            fabric.api.local(command)

        self.local_process = Process(target=run_worker)
        self.local_process.start()

    def _show_remote_collector_logs(self):
        self.tracker.step("Outputting logs of work of remote collector...")

        fabric.api.run('cat {0}'.format(self.basic_log_filename))
        fabric.api.run('cat {0}'.format(self.error_log_filename))

    def _download_csv_file(self):

        self.tracker.step("Downloading remote CSV to local host...")

        fabric.api.run('gzip -c {0} > {0}.gz'.format(self.outfile))

        # Create ./data/ dir and download remote CSV to it
        fabric.api.local('mkdir -p data')
        fabric.api.get(self.outfile + '.gz', './data/')
        fabric.api.local('gzip -d {0}.gz'.format(
            os.path.join(os.getcwd(), self.outfile)
        ))

    def _reindex_sphinx(self):

        self.tracker.step("Execute re-indexing of Sphinx...")
        fabric.api.local('indexer {0} --rotate'.format(settings.SPHINX_GROUPS_INDEX))

    def pre(self):
        super(GroupsUpdater, self).pre()

        if self.is_local:
            fabric.api.local('mkdir -p data')
        else:
            self._put_executables()
            fabric.api.run('mkdir -p data')

        if not self.is_debug and settings.UPDATING_GROUPS_COUNT is None:
            self.groups_count = self._get_vk_groups_count()
        else:
            self.groups_count = settings.UPDATING_GROUPS_COUNT

    def run(self):
        super(GroupsUpdater, self).run()

        if self.is_local:
            self._local_run()
        else:
            self._remote_run()

    def is_done(self):

        if self.is_local:
            return not self.local_process.is_alive()
        else:
            command = 'ps -C "python ./autoupdates/collectors/groups.py"'
            response = fabric.api.run(command, quiet=True)

            # Number of running processes
            return len(response.split('\n')) <= 1

    def get_progress(self):

        command = 'python ./autoupdates/collectors/groups.py --collected_data {0} last_gid'.format(
            self.outfile
        )
        try:
            if self.is_local:
                response = fabric.api.local(command, capture=True)
            else:
                response = fabric.api.run(command, quiet=True)

            current_gid = int(response)
            return Progress(current=current_gid, all=self.groups_count)
        except:
            return None

    def post(self):
        super(GroupsUpdater, self).post()

        if not self.is_local:
            self._download_csv_file()
            self._show_remote_collector_logs()

        self._import_data()
        self._cleanup()
        self._reindex_sphinx()

        self.tracker.finish()
