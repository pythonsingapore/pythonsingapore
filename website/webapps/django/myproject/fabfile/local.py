"""Fabric commands that are run locally."""
import os

from fabric.api import lcd, local, settings
from fabric.colors import _wrap_with

from myproject.settings import (
    DATABASES,
    MEDIA_ROOT,
    PROJECT_ROOT,
)
from fabfile import fab_settings


GREEN_BG = _wrap_with('42')
RED_BG = _wrap_with('41')


def check():
    """Checks if the current state can be pushed."""
    flake8()
    test()


def delete_db():
    """Deletes all data in the database."""
    local(' ./manage.py reset_db --router=default --noinput')


def dumpdata():
    """Dumps everything.

    Remember to add new dumpdata commands for new apps here so that you always
    get a full initial dump when running this task.

    """
    local('python2.7 ./manage.py dumpdata --indent 4 --natural auth'
          ' --exclude auth.permission > myproject/'
          'fixtures/bootstrap_auth.json')

    local('python2.7 ./manage.py dumpdata --indent 4 --natural registration >'
          ' myproject/fixtures/bootstrap_registration.json')

    local('python2.7 ./manage.py dumpdata --indent 4 --natural sites >'
          'myproject/fixtures/bootstrap_sites.json')

    local('python2.7 ./manage.py dumpdata --indent 4 --natural cms.placeholder'
          ' > myproject/fixtures/bootstrap_cms.json')

    local('python2.7 ./manage.py dumpdata --indent 4 --natural cms'
          ' --exclude cms.placeholder > myproject/fixtures/'
          'bootstrap_cms2.json')

    local('python2.7 ./manage.py dumpdata --indent 4 --natural text >'
          ' myproject/fixtures/bootstrap_cms_plugins_text.json')

    local('python2.7 ./manage.py dumpdata --indent 4 --natural cmsplugin_blog'
          ' > myproject/fixtures/bootstrap_cmsplugin_blog.json')

    local('python2.7 ./manage.py dumpdata --indent 4 --natural tagging >'
          ' myproject/fixtures/bootstrap_tagging.json')


def export_db():
    """Exports the database."""
    db_engine = DATABASES['default']['ENGINE']
    db_user = DATABASES['default']['USER']
    db_name = DATABASES['default']['NAME']
    db_password = DATABASES['default']['PASSWORD']
    if 'sqlite' in db_engine:
        print('You are using sqlite3, no need to export anything.')
    if 'postgre' in db_engine:
        local('pg_dump -c -U {0} > {1}_psql.sql'.format(db_user, db_name))
    if 'mysql' in db_engine:
        local('mysqldump -u{0} -p {1} {2} > {2}_mysql.sql'.format(
            db_user, db_password, db_name))


def flake8():
    """Searches for PEP8 errors in all project files."""
    local("flake8 --statistics .")


def import_db():
    """Imports the database."""
    db_engine = DATABASES['default']['ENGINE']
    db_user = DATABASES['default']['USER']
    db_name = DATABASES['default']['NAME']
    db_password = DATABASES['default']['PASSWORD']
    if 'sqlite' in db_engine:
        print('You are using sqlite3, no need to import anything.')
    if 'postgre' in db_engine:
        local('psql -U {0} < {1}_psql.sql'.format(db_user, db_name))
    if 'mysql' in db_engine:
        local('mysql -u{0} -p{1} {2} < {2}_mysql.sql'.format(
            db_user, db_password, db_name))


def lessc():
    """Compiles all less files."""
    local('lessc myproject/static/css/bootstrap.less myproject/static/css/'
          'bootstrap.css')

    local('lessc myproject/static/css/responsive.less myproject/static/css/'
          'bootstrap-responsive.css')


def push():
    """git push after checking tests and syntax"""
    check()
    local("git push")


def rebuild():
    """Deletes the database and recreates the database.

    Does not work with PostgreSQL. TODO: Create a new manage.py command
    that deletes all tables instead of the whole database.
    """
    rebuild_db()
    rebuild_media()
    local('./manage.py collectstatic --noinput')


def rebuild_db():
    """Syncdb localhost or remote server."""
    delete_db()
    local('python2.7 manage.py syncdb --all --noinput')
    local('python2.7 manage.py migrate --fake')
    local('python2.7 manage.py loaddata bootstrap_auth.json')
    local('python2.7 manage.py loaddata bootstrap_registration.json')
    local('python2.7 manage.py loaddata bootstrap_sites.json')
    local('python2.7 manage.py loaddata bootstrap_cms.json')
    local('python2.7 manage.py loaddata bootstrap_cms2.json')
    local('python2.7 manage.py loaddata bootstrap_cms_plugins_text.json')
    local('python2.7 manage.py loaddata bootstrap_cmsplugin_blog.json')
    local('python2.7 manage.py loaddata bootstrap_tagging.json')
    local('python2.7 manage.py loaddata bootstrap.json')


def rebuild_media():
    """Copies media fixtures into your media_root."""
    local('rm -rf %s' % MEDIA_ROOT)
    media_fixtures_path = os.path.join(
        PROJECT_ROOT, 'test_media/fixtures/media/')
    local('mkdir -p %s' % media_fixtures_path)
    local('cp -rf %s %s' % (media_fixtures_path, MEDIA_ROOT))


def replace_media():
    """Deletes your current media folder and unpacks the downloaded one.

    ATTENTION: All your current media files will be lost!
    You can download the latest media via ``fab run_download_media``.
    """
    with lcd('../../'):
        local('rm -rf media')
        local('mkdir media')
        local('tar -C ./media -xvf {0}_media.tar.bz2'.format(
            fab_settings.PROJECT_NAME))


def test(options=None, integration=1):
    """Runs manage.py tests::

        $ fab test                          # will run all unit tests
        $ fab test:app1                     # will run tests only for app1
        $ fab test:integration=0            # will exclude integration tests

    """
    command = ('./manage.py test -v 2 --traceback --failfast'
               ' --settings=myproject.settings.test_settings')
    if int(integration) == 0:
        command += " --exclude='integration_tests'"
    if options:
        command += ' {0}'.format(options)
    with settings(warn_only=True):
        result = local(command, capture=False)
    if result.failed:
        print RED_BG('Some tests failed')
    else:
        print GREEN_BG('All tests passed')
