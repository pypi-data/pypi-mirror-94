# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shor',
 'shor.algorithms',
 'shor.framework',
 'shor.providers',
 'shor.providers.qiskit',
 'shor.transpilers',
 'shor.utils']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.3,<4.0.0', 'numpy>=1.19.4,<2.0.0', 'qiskit>=0.23.1,<0.24.0']

setup_kwargs = {
    'name': 'shor',
    'version': '0.0.6',
    'description': 'Quantum Computing for Humans',
    'long_description': '# shor\nThe Python quantum computing library.\n\nShor is a simple, modular, and extensible quantum computing API written in python.\n\n#### Our mission is to make quantum computing easy and accesible to everyone.\n\nUse shor if you need a library that:\n- Enables fast prototyping of quantum circuits\n- Simulates small quantum programs\n- Makes quantum computing easy\n\nWe currently support running programs on Qiskit providers including IBMQ quantum computeres.\n\nIn the near future we plan to support other providers. Write your program once, and run it anywhere.\n\nRead the documentation, view tutorials and examples, and join the community at: https://shor.dev/\n\nWe are in early development and looking for contributors!\n\nWant to contribute? See [CONTRIBUTING.md](CONTRIBUTING.md)\n\nShor is compatible with Python 3.6 and is distributed under the MIT license.',
    'author': 'Collin Overbay - shor.dev',
    'author_email': 'shordotdev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
