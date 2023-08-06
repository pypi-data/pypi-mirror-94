# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastocr']

package_data = \
{'': ['*']}

install_requires = \
['PySide2>=5.15.2,<6.0.0',
 'baidu-aip>=2.2.18,<3.0.0',
 'dbus-python>=1.2.16,<2.0.0',
 'qasync>=0.13.0,<0.14.0']

entry_points = \
{'console_scripts': ['fastocr = fastocr.__main__:main']}

setup_kwargs = {
    'name': 'fastocr',
    'version': '0.1.1',
    'description': 'FastOCR is a desktop application for OCR API.',
    'long_description': None,
    'author': 'Bruce Zhang',
    'author_email': 'zttt183525594@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BruceZhang1993/FastOCR',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
