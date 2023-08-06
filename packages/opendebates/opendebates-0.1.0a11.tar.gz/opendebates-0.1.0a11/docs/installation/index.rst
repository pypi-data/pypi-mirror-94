.. _installation_index:

============
Installation
============

This bot runs on Erin which is a bot framework. Follow the `instructions here <https://erin.readthedocs.io/en/latest/installation/database.html>`_ to setup a database for Erin.

For Users
=========

For production use, please install from pip.

::

    pip install opendebates

Then verify it is working by running this command:

::

    erin -V

For Developers
==============

Installing from source
----------------------

Open Debates is very easy to install from source. First clone the latest development
version from the master branch.

::

    git clone https://github.com/OpenDebates/OpenDebates.git


Since OpenDebates has a lot of dependencies, it is wise to install a virtualenv first.
Please do not use `pipenv <https://pipenv.pypa.io/en/latest/>`_ however.
It's incompatible with Open Debates dependencies and may cause more problems in
the future. If you wish to submit a pull request to fix this problem please read more `here <https://github.com/pypa/pipenv/issues/1578>`_

First let's make a virtualenv. So we have to install it first.

::

    pip install virtualenv

Then create a new virtualenv within the repository. If you name it ``venv`` it won't get checked in.

::

    cd OpenDebates/
    virtualenv venv

Now let's activate the virtual environment.

::

    source venv/bin/activate

You should now see your terminal change to show your are you now using a virtual environment.
Let's install the package dependencies now. This may take a while depending on your machine.
Now let's install it locally as an editable installation to make sure our changes get picked up.

::

    pip install -e .

Additionally, if you need to write tests run this command.

::

    pip install -e .[TESTS]
