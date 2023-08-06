# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ecoindex']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ecoindex',
    'version': '0.5.0',
    'description': 'Ecoindex module provides a simple way to measure the Ecoindex score based on the 3 parameters: The DOM elements of the page, the size of the page and the number of external requests of the page',
    'long_description': "# ECOINDEX PYTHON\n\nThis basic module provides a simple interface to get the [Ecoindex](http://www.ecoindex.fr) based on 3 parameters:\n\n- The number of DOM elements in the page\n- The size of the page\n- The number of external requests of the page\n\n## Requirements\n\n- Python ^3.8\n\n## Install\n\n```shell\npip install ecoindex\n```\n\n## Use\n\n```python\nfrom ecoindex import get_ecoindex\nfrom pprint import pprint\n\nresult = get_ecoindex(dom=100, size=100, requests=100)\npprint(result)\n```\n\n```python\nEcoindex(grade='B', score=67, ges=1.66, water=2.49)\n```\n\n## Tests\n\n```shell\npytest\n```\n",
    'author': 'Vincent Vatelot',
    'author_email': 'vincent.vatelot@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://www.ecoindex.fr',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
