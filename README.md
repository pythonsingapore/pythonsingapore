# pythonsingapore.com

This repository holds the source code of the website [www.pythonsingapore.com](https://www.pythonsingapore.com).

# How to setup this project locally

## Prerequisites

You need to install at least the following tools in order to run this project
locally:

    sudo apt-get install python-dev
    sudo apt-get install python-setuptools
    sudo apt-get install git-core git
    sudo apt-get install mercurial
    sudo apt-get install sqlite3
    sudo apt get install libsqlite3-dev
    sudo apt get install postgresql
    sudo apt-get install pgdmin3
    sudo apt-get install python-psycopg2

## Install the project locally

Fork this repository, then clone your fork. Don't forget to initialize the
submodules in your local clone:

    git submodule init
    git submodule update

Next you should create a virtual environment for your local development:

    mkvirtualenv -p python2.7 pysg

Next install all required packages. This will take quite some time:

    workon pysg
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

If you found a bug or event want to implement a whole new feature, please do
the following:

1. Fork this repository on GitHub
2. Clone your fork into your local machine
3. Follow the instructions above
4. Create a feature branch off the master branch

        workon pysg
        git checkout -b feature_branch_name origin/master
        cd website/webapps/django/myproject
        fab rebuild

5. Implement your feature. Make sure that your code is PEP8 compliant,
   that the tests always run and that coverage stays at 100%

        workon pysg
        cd website/webapps/django/myproject
        fab flake8
        fab test

6. If your feature takes a long time to implement, make sure to regularily
   rebase the master branch to keep merge conflicts at a minimum. This is a
   bit tricky because in order to do so you need to fast forward your local
   master branch to the latest master branch of the mail repository first:

        git checkout -b upstream/master
        git remote add upstream git://github.com/pythonsingapore/pythonsingapore.git
        # The part above this line only has to be done once

        # From then on, in order to syncronize your own fork's master:
        git checkout upstream/master
        git pull upstream master
        git checkout master  # this is your own fork's master
        git merge upstream/master
        git push origin master
        git checkout feature_branch_name
        git rebase master
        # fix any merge conflicts

7. Please make sure that your commit messages consist of one line describing
   your change briefly. If you have more to say, add a blank line and then your
   longer description. No line should have more than 80 characters. Example:

        Added DISQUS script to the news detail template

        NOTE: In order for this to work you need to disable the new DISQUS 2012
        settings in your DISQUS account.

8. When your change is ready to be merged back into the main repository send us
   a pull request via GitHub. We will do a codereview and if all goes well we
   will merge your pull request and add you to the AUTHORS file. After that
   you can delete your fork or at least your feature branch.
