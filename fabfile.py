# -*- coding: utf8 -*-
from fabric.api import sudo, run, cd, settings, put, local, env
from fabric.contrib.files import exists
from autoupdates import GroupsUpdater
from autoupdates import AnalyticsUpdater
from autoupdates import PostsUpdater
from autoupdates import JobTracker

import settings as global_settings
import time
import os
import logging


USER = 'anmec2'
HOST = 'anmec.valt.me'
ADMIN_USER = 'nikolay'
BRANCH = 'develop'

env.hosts = [HOST]
env.user = USER


def get_local_path(path):
    return os.path.join(os.path.dirname(__file__), path)


def get_dirs(username):
    """ Return dict of user dirs """

    home_dir = '/home/%s/' % username
    return dict(
        home = home_dir,
        ssh  = os.path.join(home_dir, '.ssh'),
        http = os.path.join(home_dir, 'http'),
        logs = os.path.join(home_dir, 'logs'),
        env  = os.path.join(home_dir, 'http/.env'),
        pip  = os.path.join(home_dir, '.pip'),
        sphinx = os.path.join(home_dir, '.sphinx_data')
    )


def prepare_create_user_env(username=USER, admin_user=ADMIN_USER):
    """ Create user environment """
    env.user = admin_user

    dirs = get_dirs(username)

    # install all the necessary packages
    sudo('apt-get update')
    sudo('aptitude install nginx supervisor mercurial postgresql python-psycopg2 build-essential python-pip python2.7-dev libpq-dev sphinxsearch')
    sudo('pip install virtualenv')

    # add user
    with settings(warn_only=True):
        sudo('adduser %s' % username)
        sudo('adduser %s pubkey' % username)
        sudo('adduser www-data %s' % username)

        sudo('/etc/init.d/nginx restart')

    # create his directory tree
    with settings(warn_only=True):
        sudo('mkdir ' + dirs['http'])
        sudo('mkdir ' + dirs['logs'])
        sudo('mkdir ' + dirs['ssh'])
        sudo('mkdir ' + dirs['pip'])
        sudo('mkdir ' + dirs['sphinx'])

    # user owns ~/.sphinx_data
    sudo("chown %s:%s %s" % (username, username, dirs['sphinx']))

    # user owns ~/.pip
    sudo("chown %s:%s %s" % (username, username, dirs['pip']))

    # Root owns home dir
    sudo('chown root:root %s' % dirs['home'])

    # user owns ~/http dir
    sudo('chown %s:%s %s' % (username, username, dirs['http']))

    # both root and user own  ~/log dir, but user can't write
    sudo('chown root:%s %s' % (username, dirs['logs']))
    sudo('chmod 750 %s %s' %  (dirs['http'], dirs['logs']))

    # upload admin key
    sudo('chmod 777 %s' % dirs['ssh'])

    with cd(dirs['ssh']):
        if exists('authorized_keys'):
            sudo('unlink authorized_keys')
        put("~/.ssh/id_rsa.pub", "authorized_keys", mode=0644)
        sudo('chown root:root authorized_keys')

        if exists('id_rsa'):
            sudo('unlink id_rsa')
            sudo('unlink id_rsa.pub')

        put(get_local_path('./conf/id_deploy'), 'id_rsa', mode=0664)
        put(get_local_path('./conf/id_deploy.pub'), 'id_rsa.pub', mode=0664)

        sudo('chown root:%s id_rsa' % (username))
        sudo('chown root:%s id_rsa.pub' % (username))

        sudo('touch known_hosts')
        sudo('chown root:%s known_hosts' % (username))
        sudo('chmod 664 known_hosts')


    sudo('chmod 755 %s' % dirs['ssh'])

def prepare_upload_code(username=USER, admin_user=ADMIN_USER):
    """ Upload code to recently created user environment """
    env.user = username

    dirs = get_dirs(username)

    # Upload code
    with cd(dirs['http']):
        if exists('.hg') is False:
            run('hg init')
        run('hg pull ssh://hg@bitbucket.org/hodik/anmec2')
        run('hg up ' + BRANCH)

    # Create virtualenv and install PIP requirements
    run('virtualenv %s' % dirs['env'])
    run('source %s' % os.path.join(dirs['env'], 'bin/activate'))

def prepare_install_server_files(username=USER, admin_user=ADMIN_USER):
    """ Copy system files and restart daemons """
    env.user = admin_user

    dirs = get_dirs(username)

    with cd(dirs['http']):
        sudo('cp ./conf/anmec2.nginx.conf      /etc/nginx/sites-enabled/')
        sudo('cp ./conf/anmec2.supervisor.conf /etc/supervisor/conf.d/')
        sudo('cp ./conf/sphinx.conf            /etc/sphinxsearch/')


    sudo('/etc/init.d/nginx reload')
    sudo('/etc/init.d/supervisor stop')
    sudo('/etc/init.d/supervisor start')
    sudo('service sphinxsearch restart')


def prepare_server(username=USER, admin_user=ADMIN_USER):
    """ Prepare server for working """
    env.user = admin_user

    prepare_create_user_env(username)
    prepare_upload_code(username)
    update_pip(username)
    prepare_install_server_files(username)


def update_pip(username=None, admin_user=ADMIN_USER):
    """ Install new packages from PIP """
    if username is not None:
        env.user = username

    with cd("~/http/"):
        run(".env/bin/pip install -U -r ./pip.reqs")

def test():
    """ Test """

    try:
        local('./manage.py test')
    except:
        pass

    local('testacular start ./client/test/testacular.conf.js')

def deploy():
    """ Deployment """

    with settings(warn_only=True):
        local('hg push --new-branch')
    with cd("~/http/"):
        run("hg pull ssh://hg@bitbucket.org/hodik/anmec2")
        run("hg up " + BRANCH)
        run(".env/bin/python manage.py syncdb")
        run(".env/bin/python manage.py migrate")
        run("killall python")


def update(job=''):
    """
    Update data
    fab update:groups
    """
    updater = None
    tracker = None

    if job == 'groups':
        tracker = JobTracker(global_settings.UPDATING_TRACKERS['groups'])
        updater = GroupsUpdater(tracker)
    elif job == 'analytics':
        tracker = JobTracker(global_settings.UPDATING_TRACKERS['analytics'])
        updater = AnalyticsUpdater(tracker)
    elif job == 'posts':
        tracker = JobTracker(global_settings.UPDATING_TRACKERS['posts'])
        updater = PostsUpdater(tracker)

    if updater is None:
        raise Exception("Unknown target")

    logging.basicConfig(level=logging.INFO)

    tracker.start('update:' + job)
    tracker.step("Updating %s started", job)

    updater.pre()
    updater.run()
    while not updater.is_done():
        progress = updater.get_progress()

        if progress is not None:
            logging.info("Progress: %s of %s", progress.current, progress.all)
        else:
            logging.info("Progress isn't unavailable at the moment")

        tracker.progress(progress)

        time.sleep(global_settings.UPDATER_SLEEP_TIME)
    updater.post()
