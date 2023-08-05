# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['msgpacketizer']

package_data = \
{'': ['*']}

install_requires = \
['cobs>=1.1,<2.0', 'crc8>=0.1,<0.2', 'msgpack>=1.0,<2.0']

setup_kwargs = {
    'name': 'msgpacketizer',
    'version': '0.2.0',
    'description': 'https://github.com/hideakitai/MsgPacketizer protocol encoding/decoding for python',
    'long_description': None,
    'author': 'Eero af Heurlin',
    'author_email': 'eero.afheurlin@iki.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
