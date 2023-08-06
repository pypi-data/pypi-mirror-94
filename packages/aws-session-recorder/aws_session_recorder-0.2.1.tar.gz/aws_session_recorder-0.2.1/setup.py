# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_session_recorder',
 'aws_session_recorder.lib',
 'aws_session_recorder.lib.schema']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy-Utils>=0.36.8,<0.37.0',
 'SQLAlchemy>=1.3.23,<2.0.0',
 'boto3>=1.17.3,<2.0.0',
 'datasette>=0.54.1,<0.55.0',
 'sqlite-utils>=3.4.1,<4.0.0']

extras_require = \
{'cli': ['ipython>=7.20.0,<8.0.0', 'typer>=0.3.2,<0.4.0']}

entry_points = \
{'console_scripts': ['asr = aws_session_recorder.main:app']}

setup_kwargs = {
    'name': 'aws-session-recorder',
    'version': '0.2.1',
    'description': 'AWS session that records discovered resources to a database',
    'long_description': None,
    'author': 'Ryan Gerstenkorn',
    'author_email': 'ryan.gerstenkorn@rhinosecuritylabs.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
