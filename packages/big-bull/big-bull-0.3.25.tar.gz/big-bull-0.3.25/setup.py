# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['big_bull']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.3,<4.0.0',
 'aiokafka>=0.7.0,<0.8.0',
 'jaeger-client>=4.4.0,<5.0.0',
 'opentracing-instrumentation>=3.3.1,<4.0.0',
 'opentracing>=2.4.0,<3.0.0',
 'prometheus-client>=0.9.0,<0.10.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['big-bull = big_bull.big_bull:main']}

setup_kwargs = {
    'name': 'big-bull',
    'version': '0.3.25',
    'description': 'Web framework for writing asynchronous microservices',
    'long_description': '# Big-bull\n\nMicro-framework wrapping aiohttp, aiokafka, jaeger and prometheus primarily\naimed towards writing kubernetes services.\n',
    'author': 'Buster Styren',
    'author_email': 'buster.styren@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
