# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jenkins_job_manager']

package_data = \
{'': ['*'], 'jenkins_job_manager': ['j2_templates/*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'jenkins-job-builder>=3.5.0,<4.0.0',
 'jinja2>=2.11,<3.0',
 'python-jenkins>=1.7.0,<2.0.0']

entry_points = \
{'console_scripts': ['jjm = jenkins_job_manager.cli:jjm']}

setup_kwargs = {
    'name': 'jenkins-job-manager',
    'version': '0.6.0',
    'description': 'A terraform-like wrapper around JJB with some additional features.\n',
    'long_description': None,
    'author': 'Jeremy Lavergne',
    'author_email': 'github@lavergne.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
