# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apm_agent_utils']

package_data = \
{'': ['*']}

install_requires = \
['elastic-apm>=5.8.0,<6.0.0']

setup_kwargs = {
    'name': 'apm-agent-utils',
    'version': '1.0.3',
    'description': 'This package can help you create Elastic APM instrumentations using regex',
    'long_description': '## Elastic APM Agent Utils\nThis package can help you create Elastic APM instrumentations using regex.\n\n### Dependencies\n1. `python3.6+`  \n2. `elastic-apm`  \n\n### Installation\n```sh\npip install apm-agent-utils\n```',
    'author': 'vuonglv',
    'author_email': 'it.vuonglv@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vuonglv1612/apm-agent-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
