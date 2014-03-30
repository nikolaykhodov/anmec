# -*- coding: utf8 -*-

""" Automatic updating stat regarding VK groups """

from base import Updater, Progress
from datetime import datetime
from fabric.api import env
from multiprocessing import Process
from datetime import date
from datetime import timedelta

import fabric.api
import fabric.context_managers
import os
import settings


class PostsUpdater(Updater):

    def __init__(self, tracker):

        super(PostsUpdater, self).__init__(tracker)

        self.is_local = settings.UPDATING_POSTS_HOST == ''
        self.timestamp = self._get_timestamp()

        self.gids_filename = './data/posts_gids_' + self.timestamp
        self.outfile = './data/posts_output_' + self.timestamp
        self.progress_filename = './data/posts_progress_' + self.timestamp
        self.basic_log_filename = 'posts_{0}_output.log'.format(self.timestamp)
        self.error_log_filename = 'posts_{0}_error.log'.format(self.timestamp)

        self.is_debug = settings.DEBUG

        today = date.today()
        self.date_from = (today + timedelta(days=-3)).strftime('%Y-%m-%d')

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
            self._delete_file(self.progress_filename, False)
            self._delete_file(self.basic_log_filename, False)
            self._delete_file(self.error_log_filename, False)
            self._delete_file(self.gids_filename, False)
            self._delete_file(self.outfile, False)
            self._delete_file(self.outfile + '.gz', False)

        self._delete_file(self.outfile)
        self._delete_file(self.gids_filename + '.gz')

    def _get_timestamp(self):
        now = datetime.now()
        # dd-mm-yyyy_hh-mm
        return now.strftime("%d-%m-%Y_%H-%M")

    def _set_up_env(self):
        if not self.is_local:
            env.host_string = settings.UPDATING_POSTS_HOST

            user = settings.UPDATING_POSTS_USER
            if user.find(':') >= 0:
                env.user, env.password = user.split(':')
            else:
                env.user = user

    def _create_gids_file(self):

        self.tracker.step("Creating groups file...")

        fabric.api.local('mkdir -p data')

        fabric.api.local('./manage.py export_gids {0} top'.format(
            self.gids_filename
        ))

    def _upload_gids_file(self):

        self.tracker.step("Uploading gids file...")

        fabric.api.local('gzip --quiet {0} {0}.gz'.format(self.gids_filename))

        fabric.api.run('mkdir -p ./data')
        fabric.api.put('{0}.gz'.format(self.gids_filename), './data/')
        fabric.api.run('gzip -d {0}.gz'.format(self.gids_filename))

    def _upload_executables(self):
        self.tracker.step("Uploading the executable files to remote host...")

        fabric.api.run('mkdir -p autoupdates/collectors')
        with fabric.api.lcd('autoupdates/collectors/'):
            fabric.api.put('*.py', './autoupdates/collectors/')

    def _remote_run(self):
        command = 'nohup python ./autoupdates/collectors/posts.py --gids-file {0} --progress-file {1} --from-date {2} --output {3} collect'.format(
            self.gids_filename,
            self.progress_filename,
            self.date_from,
            self.outfile
        )
        command = command + ' > {0} 2> {1} < /dev/null &'.format(
            self.basic_log_filename,
            self.error_log_filename
        )
        fabric.api.run(command, pty=False)

    def _local_run(self):

        def run_worker():
            command = 'python ./autoupdates/collectors/posts.py --gids-file {0} --progress-file {1} --from-date {2} --output {3} collect'.format(
                self.gids_filename,
                self.progress_filename,
                self.date_from,
                self.outfile
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

    def _import_data(self):
        self.tracker.step("Importing data...")

        fabric.api.local('chmod 644 {0}'.format(self.outfile))
        fabric.api.local('./manage.py import_posts {0}'.format(
            os.path.join(os.getcwd(), self.outfile)
        ))

    def _reindex_sphinx(self):

        self.tracker.step("Execute re-indexing of Sphinx...")
        fabric.api.local('indexer {0} --rotate'.format(settings.SPHINX_POSTS_INDEX))

    def pre(self):
        super(PostsUpdater, self).pre()

        # File with one gid per line
        self._create_gids_file()

        if not self.is_local:
            self._upload_gids_file()

        if self.is_local:
            fabric.api.local('mkdir -p data')
        else:
            self._upload_executables()
            fabric.api.run('mkdir -p data')

    def run(self):
        super(PostsUpdater, self).run()

        if self.is_local:
            self._local_run()
        else:
            self._remote_run()

    def is_done(self):

        if self.is_local:
            return not self.local_process.is_alive()
        else:
            command = 'ps -C "python ./autoupdates/collectors/posts.py"'
            response = fabric.api.run(command, quiet=True)

            # Number of running processes
            print(response)
            return len(response.split('\n')) <= 1

    def get_progress(self):

        command = 'cat {0}'.format(
            self.progress_filename
        )
        try:
            if self.is_local:
                response = fabric.api.local(command, capture=True)
            else:
                response = fabric.api.run(command, quiet=True)

            parts = response.split('/')
            current_group, all_groups = int(parts[0]), int(parts[1])
            return Progress(current=current_group, all=all_groups)
        except:
            return None

    def post(self):
        super(PostsUpdater, self).post()

        if not self.is_local:
            self._show_remote_collector_logs()
            self._download_csv_file()

        self._import_data()
        self._cleanup()
        self._reindex_sphinx()

        self.tracker.finish()
