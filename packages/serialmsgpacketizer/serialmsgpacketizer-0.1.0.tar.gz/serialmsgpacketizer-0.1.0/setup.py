# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['serialmsgpacketizer']

package_data = \
{'': ['*']}

install_requires = \
['datastreamservicelib>=1.8.0,<2.0.0', 'pyserial>=3.5,<4.0']

entry_points = \
{'console_scripts': ['serialmsgpacketizer = '
                     'serialmsgpacketizer.console:serialmsgpacketizer_cli']}

setup_kwargs = {
    'name': 'serialmsgpacketizer',
    'version': '0.1.0',
    'description': 'Send & Receive MsgPacketizer packets over serial link',
    'long_description': '===================\nserialmsgpacketizer\n===================\n\nSend & Receive MsgPacketizer packets over serial link.\n\nSee also https://gitlab.com/advian-oss/python-msgpacketizer\n\nDocker\n------\n\nFor more controlled deployments and to get rid of "works on my computer" -syndrome, we always\nmake sure our software works under docker.\n\nIt\'s also a quick way to get started with a standard development environment.\n\nSSH agent forwarding\n^^^^^^^^^^^^^^^^^^^^\n\nWe need buildkit_::\n\n    export DOCKER_BUILDKIT=1\n\n.. _buildkit: https://docs.docker.com/develop/develop-images/build_enhancements/\n\nAnd also the exact way for forwarding agent to running instance is different on OSX::\n\n    export DOCKER_SSHAGENT="-v /run/host-services/ssh-auth.sock:/run/host-services/ssh-auth.sock -e SSH_AUTH_SOCK=/run/host-services/ssh-auth.sock"\n\nand Linux::\n\n    export DOCKER_SSHAGENT="-v $SSH_AUTH_SOCK:$SSH_AUTH_SOCK -e SSH_AUTH_SOCK"\n\nCreating a development container\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\nBuild image, create container and start it (switch the 51459 port to the port from src/serialmsgpacketizer/defaultconfig.py)::\n\n    docker build --ssh default --target devel_shell -t serialmsgpacketizer:devel_shell .\n    docker create --name serialmsgpacketizer_devel -p 51459:51459 -p 51460:51460 -v `pwd`":/app" -it -v /tmp:/tmp `echo $DOCKER_SSHAGENT` serialmsgpacketizer:devel_shell\n    docker start -i serialmsgpacketizer_devel\n\npre-commit considerations\n^^^^^^^^^^^^^^^^^^^^^^^^^\n\nIf working in Docker instead of native env you need to run the pre-commit checks in docker too::\n\n    docker exec -i serialmsgpacketizer_devel /bin/bash -c "pre-commit install"\n    docker exec -i serialmsgpacketizer_devel /bin/bash -c "pre-commit run --all-files"\n\nYou need to have the container running, see above. Or alternatively use the docker run syntax but using\nthe running container is faster::\n\n    docker run -it --rm -v `pwd`":/app" serialmsgpacketizer:devel_shell -c "pre-commit run --all-files"\n\nTest suite\n^^^^^^^^^^\n\nYou can use the devel shell to run py.test when doing development, for CI use\nthe "tox" target in the Dockerfile::\n\n    docker build --ssh default --target tox -t serialmsgpacketizer:tox .\n    docker run -it --rm -v `pwd`":/app" `echo $DOCKER_SSHAGENT` serialmsgpacketizer:tox\n\nProduction docker\n^^^^^^^^^^^^^^^^^\n\nThere\'s a "production" target as well for running the application (change the "51459" port and "myconfig.toml" for\nconfig file)::\n\n    docker build --ssh default --target production -t serialmsgpacketizer:latest .\n    docker run -it --name serialmsgpacketizer -v myconfig.toml:/app/config.toml -p 51459:51459 -p 51460:51460 -it -v /tmp:/tmp `echo $DOCKER_SSHAGENT` serialmsgpacketizer:latest\n\n\nLocal Development\n-----------------\n\nTLDR:\n\n- Create and activate a Python 3.7 virtualenv (assuming virtualenvwrapper)::\n\n    mkvirtualenv -p `which python3.7` my_virtualenv\n\n- change to a branch::\n\n    git checkout -b my_branch\n\n- install Poetry: https://python-poetry.org/docs/#installation\n- Install project deps and pre-commit hooks::\n\n    poetry install\n    pre-commit install\n    pre-commit run --all-files\n\n- Ready to go, try the following::\n\n    serialmsgpacketizer --defaultconfig >config.toml\n    serialmsgpacketizer -vv config.toml\n\nRemember to activate your virtualenv whenever working on the repo, this is needed\nbecause pylint and mypy pre-commit hooks use the "system" python for now (because reasons).\n\nRunning "pre-commit run --all-files" and "py.test -v" regularly during development and\nespecially before committing will save you some headache.\n',
    'author': 'Eero af Heurlin',
    'author_email': 'eero.afheurlin@iki.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/advian-oss/python-serialmsgpacketizer/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
