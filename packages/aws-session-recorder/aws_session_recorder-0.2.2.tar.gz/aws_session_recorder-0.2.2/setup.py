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
{'console_scripts': ['aws-session-recorder = aws_session_recorder.main:app']}

setup_kwargs = {
    'name': 'aws-session-recorder',
    'version': '0.2.2',
    'description': 'AWS session that records discovered resources to a database',
    'long_description': '====================\naws-session-recorder\n====================\n\n\n.. image:: https://img.shields.io/pypi/v/aws_session_recorder.svg\n        :target: https://pypi.python.org/pypi/aws_session_recorder\n\n.. image:: https://github.com/RyanJarv/aws_session_recorder/workflows/Python%20package/badge.svg\n        :target: https://github.com/RyanJarv/aws_session_recorder/actions\n\n.. image:: https://readthedocs.org/projects/aws-session-recorder/badge/?version=latest\n        :target: https://aws-session-recorder.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\n\n\nAWS session that records discovered resources to a database\n\nNOTE: This project is still a work in progress.\n\n\n* Free software: BSD license\n* Documentation: https://aws-session-recorder.readthedocs.io.\n\n\nFeatures\n--------\n\n* Works just like a normal boto3 session, so you can use it for any library that allows you to set the boto3 session..\n* Records IAM related Get/List requests to a local sqlite.db.\n* Use datasette to view recorded data.\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage\n',
    'author': 'Ryan Gerstenkorn',
    'author_email': 'ryan.gerstenkorn@rhinosecuritylabs.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://aws-session-recorder.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
