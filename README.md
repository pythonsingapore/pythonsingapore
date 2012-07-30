# pythonsingapore.com

This repository holds the source code of the website [pythonsingapore.com](https://pythonsingapore.com).

# How to setup this project locally

Fork this repository, then clone your fork. Next you should create a virtual
environment for your local development:

    mkvirtualenv -p python2.7 pysg

Next install all required packages. This will take quite some time:

    pip install -r website/webapps/django/myproject/requirements.txt --upgrade

Once your virtual environment is fully installed, please create your local
settings files:

    cd website/webapps/django/myproject/myproject/settings/local/
    cp local_settings.py.sample local_settings.py

The standard settings use sqlite3 and will work fine but you should have a look
at that file if you plan to submit a bigger contribution. You should create a
postgres database locally and add your database settings accordingly.

Finally you need to copy the `fab_settings.py.sample` in order to use our
fabfile:

    cd website/webapps/django/myproject/fabfile/
    cp fab_settings.py.sample fab_settings.py

If you are using OSX, please change the setting `WWW_OPEN` to `open`. Otherwise
you should now be able to install your local database with some boostrap
fixtures:

    cd website/webapps/django/myproject/
    workon pysg
    fab rebuild
    ./mange.py runserver

You should now see our site with nice test data available. The admin user is
called `admin` and the password is `test123`.

# How to contribute

Coming soon
