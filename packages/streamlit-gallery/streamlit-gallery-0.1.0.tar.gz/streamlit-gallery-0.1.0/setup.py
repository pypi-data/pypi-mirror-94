# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamlit_gallery']

package_data = \
{'': ['*']}

install_requires = \
['spacy>=3.0.1,<4.0.0', 'streamlit>=0.76.0,<0.77.0']

setup_kwargs = {
    'name': 'streamlit-gallery',
    'version': '0.1.0',
    'description': 'Streamlit gallery.',
    'long_description': None,
    'author': 'Yevgnen Koh',
    'author_email': 'wherejoystarts@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
