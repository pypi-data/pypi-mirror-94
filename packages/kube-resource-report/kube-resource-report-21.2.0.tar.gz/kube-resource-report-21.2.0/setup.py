# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kube_resource_report']

package_data = \
{'': ['*'],
 'kube_resource_report': ['templates/*',
                          'templates/assets/*',
                          'templates/partials/*']}

install_requires = \
['jinja2', 'pykube-ng', 'requests', 'requests-futures', 'stups-tokens']

entry_points = \
{'console_scripts': ['kube-resource-report = kube_resource_report:main.main']}

setup_kwargs = {
    'name': 'kube-resource-report',
    'version': '21.2.0',
    'description': 'Report Kubernetes cluster and pod resource requests vs usage and generate static HTML',
    'long_description': None,
    'author': 'Henning Jacobs',
    'author_email': 'henning@jacobs1.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://codeberg.org/hjacobs/kube-resource-report',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
