# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['qr_code_generator']
install_requires = \
['PyQRCode>=1.2.1,<2.0.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['qr-code = qr_code_generator:app']}

setup_kwargs = {
    'name': 'qr-code-generator',
    'version': '0.1.0',
    'description': 'QR code generator for URLs i.e. dynamic QR codes.',
    'long_description': None,
    'author': 'Marcelo Trylesinski',
    'author_email': 'marcelotryle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
