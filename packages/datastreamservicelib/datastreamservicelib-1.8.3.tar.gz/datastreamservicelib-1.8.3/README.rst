====================
datastreamservicelib
====================

AsyncIO eventloop helpers and Abstract Base Classes for making services that use ZMQ nice, easy and DRY

Usage
-----

Use the CookieCutter template at https://gitlab.com/advian-oss/python-datastreamserviceapp_template

You can also take a look at src/datastreamservicelib/console.py for some very simple test examples.


Development
-----------

TLDR:

- create Python 3.7 virtualenv and activate it (pro tip: virtualenvwrapper)
- poetry install
- pre-commit install


Testing
^^^^^^^

There's Dockerfile for running tox tests (so you don't need to deal with pyenv
and having all the required versions available)::

    docker build -t datastreamservicelib:tox .
    docker run --rm -it -v `pwd`:/app datastreamservicelib:tox
