# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['si_utils',
 'si_utils._vendor',
 'si_utils._vendor.boltons',
 'si_utils._vendor.toml']

package_data = \
{'': ['*']}

install_requires = \
['loguru']

extras_require = \
{'dev-utils': ['tomlkit', 'semver', 'pytest'],
 'sentry': ['sentry-sdk>=0.19,<0.20'],
 'yaml': ['ruamel.yaml', 'deepmerge', 'pydantic']}

setup_kwargs = {
    'name': 'si-utils',
    'version': '0.3.0',
    'description': 'an opinionated set of utilities designed to be easily included in any number of projects',
    'long_description': '# About\n\nThis package contains a set of utilities useful for building python libraries, scripts, and command-line utilities\n\nIt\'s designed to be easy to include in other projects. all of its mainline dependencies are vendored and all modules which have external un-vendorable dependencies are available as optional extras\n\n# Install\n\n```\npip install si-utils\n```\n\nTo make use of optional extras, like the yaml module or the dev_utils module:\n\n```\npip install si-utils[yaml] # or si-utils[dev_utils], or si-utils[yaml,sentry]\n```\n\n# Usage\n\nThis toolkit makes it really easy to write small, simple, well designed CLI utilities\nIn fact, the aim of this project is to make well-engineered CLIs almost as easy to write and deploy as basic python scripts\nit leverages a lot of really fantastic modern libraries and tools to do so, like *poetry*, *typer*, and *loguru*\n\nlet\'s assume you\'ve created a new project with `poetry new`, and you want to add a CLI interface to it. here\'s one way to do that:\ncreate a `common.py` files with your super handy dandy useful function in it:\n```python\nfrom loguru import logger\n\ndef my_super_awesome_function():\n    logger.debug("I\'m running my_package.common.my_super_awesome_function!")\n\n```\n\ncreate a `__main__.py` file in your package like so:\n```python\nimport os\n\nfrom .common import my_super_awesome_function\n\nimport si_utils\nimport typer\nfrom loguru import logger\n\napp = typer.Typer()\n\n\n@app.callback()\ndef callback(verbose: bool = False):\n    """\n    Here is my app\'s main help string\n    Users will see this when they run `python -m my_package`\n    """\n    log_level = \'DEBUG\' if verbose else \'INFO\'\n    si_utils.configure_logging(\n        \'my_app_name\', \n        stderr_level=log_level, \n        logfile_level=\'DEBUG\', \n        sentry_level=None)\n\n\n@app.command()\ndef my_command(option: bool):\n    """\n    Here\'s the help text my users will see when they run `python -m my_package my-command -h`\n    """\n    logger.debug("running my-command")  # this will only get printed if the --verbose flag is set\n    my_super_awesome_function(option)\n\n\nif __name__ == "__main__":\n    if os.environ.get(\'PYDEBUG\'):\n        # we\'re in a debugger session\n        # here we can put whatever debugging code we want\n        # we can configure logging so all messages up to DEBUG are logged to stderr, and nothing gets logged to file:\n        configure_logging(\'my_app_name\', \'DEBUG\', None, None)\n        # do debugging stuff here\n        logger.debug("I\'m a debug message!")\n        exit()\n    try:\n        app()  # cli code goes here\n    except KeyboardInterrupt:\n        print("Aborted!")\n        exit()\n\n```\n\nthe main api (all the stuff directly importable from `si_utils`) consists of:\n- every function defined in the `main` module\n- the `configure_logging` function from the `log` module\n\n`configure_logging` has an option to enable logging to sentry. in order to use it, you need to install si_utils with the `sentry` extra (ie `pip install si-utils[sentry]` or `poetry add -D si-utils[sentry]`)\n\napart from that, there are other modules which can be imported separately:\n\n`yaml` has a whole bunch of useful and sometimes esoteric utilities for working with yaml files, built on top of `ruamel.yaml`\n\n`dev_utils` has commmand-line utilities for working with python projects, specifically made for projects that use `poetry`',
    'author': 'Alex Tremblay',
    'author_email': 'alex.tremblay@utoronto.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
