===================
serialmsgpacketizer
===================

Send & Receive MsgPacketizer packets over serial link.

See also https://gitlab.com/advian-oss/python-msgpacketizer

Docker
------

For more controlled deployments and to get rid of "works on my computer" -syndrome, we always
make sure our software works under docker.

It's also a quick way to get started with a standard development environment.

SSH agent forwarding
^^^^^^^^^^^^^^^^^^^^

We need buildkit_::

    export DOCKER_BUILDKIT=1

.. _buildkit: https://docs.docker.com/develop/develop-images/build_enhancements/

And also the exact way for forwarding agent to running instance is different on OSX::

    export DOCKER_SSHAGENT="-v /run/host-services/ssh-auth.sock:/run/host-services/ssh-auth.sock -e SSH_AUTH_SOCK=/run/host-services/ssh-auth.sock"

and Linux::

    export DOCKER_SSHAGENT="-v $SSH_AUTH_SOCK:$SSH_AUTH_SOCK -e SSH_AUTH_SOCK"

Creating a development container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Build image, create container and start it (switch the 51459 port to the port from src/serialmsgpacketizer/defaultconfig.py)::

    docker build --ssh default --target devel_shell -t serialmsgpacketizer:devel_shell .
    docker create --name serialmsgpacketizer_devel -p 51459:51459 -p 51460:51460 -v `pwd`":/app" -it -v /tmp:/tmp `echo $DOCKER_SSHAGENT` serialmsgpacketizer:devel_shell
    docker start -i serialmsgpacketizer_devel

pre-commit considerations
^^^^^^^^^^^^^^^^^^^^^^^^^

If working in Docker instead of native env you need to run the pre-commit checks in docker too::

    docker exec -i serialmsgpacketizer_devel /bin/bash -c "pre-commit install"
    docker exec -i serialmsgpacketizer_devel /bin/bash -c "pre-commit run --all-files"

You need to have the container running, see above. Or alternatively use the docker run syntax but using
the running container is faster::

    docker run -it --rm -v `pwd`":/app" serialmsgpacketizer:devel_shell -c "pre-commit run --all-files"

Test suite
^^^^^^^^^^

You can use the devel shell to run py.test when doing development, for CI use
the "tox" target in the Dockerfile::

    docker build --ssh default --target tox -t serialmsgpacketizer:tox .
    docker run -it --rm -v `pwd`":/app" `echo $DOCKER_SSHAGENT` serialmsgpacketizer:tox

Production docker
^^^^^^^^^^^^^^^^^

There's a "production" target as well for running the application (change the "51459" port and "myconfig.toml" for
config file)::

    docker build --ssh default --target production -t serialmsgpacketizer:latest .
    docker run -it --name serialmsgpacketizer -v myconfig.toml:/app/config.toml -p 51459:51459 -p 51460:51460 -it -v /tmp:/tmp `echo $DOCKER_SSHAGENT` serialmsgpacketizer:latest


Local Development
-----------------

TLDR:

- Create and activate a Python 3.7 virtualenv (assuming virtualenvwrapper)::

    mkvirtualenv -p `which python3.7` my_virtualenv

- change to a branch::

    git checkout -b my_branch

- install Poetry: https://python-poetry.org/docs/#installation
- Install project deps and pre-commit hooks::

    poetry install
    pre-commit install
    pre-commit run --all-files

- Ready to go, try the following::

    serialmsgpacketizer --defaultconfig >config.toml
    serialmsgpacketizer -vv config.toml

Remember to activate your virtualenv whenever working on the repo, this is needed
because pylint and mypy pre-commit hooks use the "system" python for now (because reasons).

Running "pre-commit run --all-files" and "py.test -v" regularly during development and
especially before committing will save you some headache.
