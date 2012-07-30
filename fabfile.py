"""Fabfile for the ``webfaction-django-boilerplate``.

Make sure to setup your ``fabric_settings.py`` first. As a start, just copy
``fabric_settings.py.sample``.

"""
from __future__ import with_statement

from fabric.api import (
    cd,
    env,
    run,
    settings,
)
from fabric.contrib.files import append, contains,  sed

import fabric_settings as fab_settings


env.hosts = fab_settings.ENV_HOSTS
env.user = fab_settings.ENV_USER

BASHRC_SETTING1 = 'export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python2.7'
BASHRC_SETTING2 = 'export WORKON_HOME=$HOME/Envs'
BASHRC_SETTING3 = 'source /home/{0}/bin/virtualenvwrapper.sh'.format(env.user)
BASHRC_SETTING4 = 'export PIP_VIRTUALENV_BASE=$WORKON_HOME'
BASHRC_SETTING5 = 'export PIP_RESPECT_VIRTUALENV=true'

PROJECT_NAME = fab_settings.PROJECT_NAME
FILE_SCRIPT_SETTINGS = 'script-settings-{0}.sh'.format(PROJECT_NAME)
FILE_DEPLOY_WEBSITE = 'deploy-website-{0}.sh'.format(PROJECT_NAME)
FILE_PG_BACKUP = 'pg-backup-{0}.sh'.format(PROJECT_NAME)
FILE_RESTART_APACHE = 'restart-apache-{0}.sh'.format(PROJECT_NAME)
FILE_DJANGO_CLEANUP = 'django-cleanup-{0}.sh'.format(PROJECT_NAME)
FILE_CRONTAB = 'crontab-{0}.txt'.format(PROJECT_NAME)
FILE_SHOW_MEMORY = 'show-memory.sh'
FILE_PGPASS = '.pgpass-{0}'.format(PROJECT_NAME)


# ****************************************************************************
# HIGH LEVEL TASKS
# ****************************************************************************
def install_everything():
    install_server()
    first_deployment()


def first_deployment():
    run_delete_previous_attempts()
    run_create_virtualenv()
    run_clone_repo()
    run_install_scripts()
    run_install_pgpass()
    run_install_crontab()
    run_delete_django()
    run_install_requirements()
    run_deploy_website(with_manage_py=False)
    run_prepare_local_settings()
    run_deploy_website()
    run_loaddata_auth()


def install_server():
    run_install_virtualenv()
    run_install_mercurial()
    run_add_bashrc_settings()
    run_delete_index_files()


# ****************************************************************************
# REMOTE TASKS
# ****************************************************************************
def run_add_bashrc_settings():
    with cd('$HOME'):
        append('.bashrc', BASHRC_SETTING1, partial=True)
        append('.bashrc', BASHRC_SETTING2, partial=True)
        append('.bashrc', BASHRC_SETTING3, partial=True)
        append('.bashrc', BASHRC_SETTING4, partial=True)
        append('.bashrc', BASHRC_SETTING5, partial=True)


def run_clone_repo():
    run('mkdir -p $HOME/src')
    with cd('$HOME/src'):
        run('git clone {0} {1}'.format(
            fab_settings.GITHUB_REPO, PROJECT_NAME))
    with cd('$HOME/src/{0}'.format(PROJECT_NAME)):
        run('git submodule init')
        run('git submodule update')


def run_create_ssh_dir():
    with cd('$HOME'):
        with settings(warn_only=True):
            run('mkdir .ssh')
            run('touch .ssh/authorized_keys')
            run('chmod 600 .ssh/authorized_keys')
            run('chmod 700 .ssh')


def run_create_virtualenv():
    with cd('$HOME'):
        run('rm -rf $HOME/Envs/{0}'.format(fab_settings.VENV_NAME))
        run('mkvirtualenv -p python2.7 --system-site-packages {0}'.format(
            fab_settings.VENV_NAME))


def run_delete_index_files():
    run('rm -f $HOME/webapps/{0}/index.html'.format(
        fab_settings.MEDIA_APP_NAME))
    run('rm -f $HOME/webapps/{0}/index.html'.format(
        fab_settings.STATIC_APP_NAME))


def run_delete_previous_attempts():
    run('rm -rf $HOME/webapps/{0}/myproject'.format(
        fab_settings.DJANGO_APP_NAME))
    run('rm -rf $HOME/Envs/{0}/'.format(fab_settings.VENV_NAME))
    run('rm -rf $HOME/src/{0}/'.format(PROJECT_NAME))
    run('rm -rf $HOME/bin/*{0}*.*'.format(PROJECT_NAME))
    with cd('$HOME'):
        run('touch .pgpass')
        run("sed '/{0}/d' .pgpass > .pgpass_tmp".format(fab_settings.DB_NAME))
        run('mv .pgpass_tmp .pgpass')
    run('crontab -l > crontab_bak')
    run("sed '/{0}.sh/d' crontab_bak > crontab_tmp".format(
        fab_settings.PROJECT_NAME))
    run('crontab crontab_tmp')
    run('rm crontab_tmp')


def run_deploy_website(with_manage_py=True):
    args = ' 1'
    if with_manage_py:
        args = ''

    run('workon {0} && deploy-website-{1}.sh{2}'.format(fab_settings.VENV_NAME,
        PROJECT_NAME, args))


def run_install_crontab():
    run('mkdir -p $HOME/mylogs/cron/')
    with cd('$HOME/bin/'):
        run('crontab -l > crontab_tmp')
        run('cat crontab-{0}.txt >> crontab_tmp'.format(
            PROJECT_NAME))
        run('crontab crontab_tmp')
        run('rm crontab_tmp')


def run_install_mercurial():
    with cd('$HOME'):
        run('easy_install-2.7 mercurial')


def run_install_pgpass():
    with cd('$HOME'):
        run('touch .pgpass')
        run('chmod 0600 .pgpass')
        if not contains('.pgpass', fab_settings.DB_NAME):
            run('cat {0} > .pgpass'.format(FILE_PGPASS))
        run('rm {0}'.format(FILE_PGPASS))


def run_install_requirements():
    run('workon {0} && pip install -r $HOME/src/{1}/website/webapps/django/'
        'myproject/requirements.txt --upgrade'.format(
            fab_settings.VENV_NAME, PROJECT_NAME))


def run_install_scripts():
    with cd('$HOME/src/{0}/scripts'.format(PROJECT_NAME)):
        run('git pull origin master')
        run('cp {0} $HOME/bin/{0}'.format(FILE_DEPLOY_WEBSITE))
        run('cp {0} $HOME/bin/{0}'.format(FILE_PG_BACKUP))
        run('cp {0} $HOME/bin/{0}'.format(FILE_RESTART_APACHE))
        run('cp {0} $HOME/bin/{0}'.format(FILE_DJANGO_CLEANUP))
        run('cp {0} $HOME/bin/{0}'.format(FILE_SCRIPT_SETTINGS))
        run('cp {0} $HOME/bin/{0}'.format(FILE_CRONTAB))
        run('cp {0} $HOME/bin/{0}'.format(FILE_SHOW_MEMORY))

        # This one goes to $HOME
        run('cp {0} $HOME/{0}'.format(FILE_PGPASS))

    with cd('$HOME/bin'):
        sed(FILE_SCRIPT_SETTINGS, 'INSERT_USERNAME', fab_settings.ENV_USER)
        sed(FILE_SCRIPT_SETTINGS, 'INSERT_DB_USER', fab_settings.DB_USER)
        sed(FILE_SCRIPT_SETTINGS, 'INSERT_DB_NAME', fab_settings.DB_NAME)
        sed(FILE_SCRIPT_SETTINGS, 'INSERT_DB_PASSWORD',
            fab_settings.DB_PASSWORD)
        sed(FILE_SCRIPT_SETTINGS, 'INSERT_PROJECT_NAME', PROJECT_NAME)
        sed(FILE_SCRIPT_SETTINGS, 'INSERT_DJANGO_APP_NAME',
            fab_settings.DJANGO_APP_NAME)
        sed(FILE_SCRIPT_SETTINGS, 'INSERT_VENV_NAME', fab_settings.VENV_NAME)
        run('rm -f *.bak')

    with cd('$HOME'):
        sed(FILE_PGPASS, 'INSERT_DB_NAME', fab_settings.DB_NAME)
        sed(FILE_PGPASS, 'INSERT_DB_USER', fab_settings.DB_USER)
        sed(FILE_PGPASS, 'INSERT_DB_PASSWORD', fab_settings.DB_PASSWORD)


def run_install_virtualenv():
    with cd('$HOME'):
        run('mkdir -p $HOME/lib/python2.7')
        run('easy_install-2.7 pip')
        run('pip install virtualenv')
        run('pip install virtualenvwrapper')
        run('mkdir -p $HOME/Envs')


def run_loaddata_auth():
    with cd('$HOME/webapps/{0}/myproject/'.format(
            fab_settings.DJANGO_APP_NAME)):

        run('workon {0} && ./manage.py loaddata bootstrap_auth.json'.format(
            fab_settings.VENV_NAME))


def run_prepare_local_settings():
    with cd('$HOME/webapps/{0}/myproject/myproject/settings/local'.format(
        fab_settings.DJANGO_APP_NAME)):
        run('cp local_settings.py.sample local_settings.py')
        sed('local_settings.py', 'backends.sqlite3',
            'backends.postgresql_psycopg2')
        sed('local_settings.py', 'db.sqlite', fab_settings.DB_NAME)
        sed('local_settings.py', '"USER": ""', '"USER": "{0}"'.format(
            fab_settings.DB_USER))
        sed('local_settings.py', '"PASSWORD": ""', '"PASSWORD": "{0}"'.format(
            fab_settings.DB_PASSWORD))
        sed('local_settings.py', 'yourproject', '{0}'.format(
            PROJECT_NAME))

        sed('local_settings.py', "'media')", fab_settings.MEDIA_APP_NAME)
        sed('local_settings.py', "'static')", fab_settings.STATIC_APP_NAME)
        sed('local_settings.py', 'yourname', fab_settings.ADMIN_NAME)
        sed('local_settings.py', 'info@example.com', fab_settings.ADMIN_EMAIL)
        run('rm -f *.bak')


def run_delete_django():
    with cd('$HOME/webapps/{0}/lib/python2.7/'.format(
        fab_settings.DJANGO_APP_NAME)):
        run('rm -rf django')
        run('rm -rf Django*')
