=================
datastreamcorelib
=================

Core helpers and Abstract Base Classes for making use of ZMQ nice, easy and DRY.

You should probably look at https://gitlab.com/advian-oss/python-datastreamservicelib and
https://gitlab.com/advian-oss/python-datastreamserviceapp_template unless you're working
on an adapter for yet unsupported eventloop.

Development
-----------

TLDR:

- make virtualenv
- poetry install
- pre-commit install

Testing
^^^^^^^

There's Dockerfile for running tox tests (so you don't need to deal with pyenv
and having all the required versions available)::

    docker build -t datastreamcorelib:tox .
    docker run --rm -it -v `pwd`:/app datastreamcorelib:tox
