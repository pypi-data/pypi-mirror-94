# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['photoscanner']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0',
 'imutils>=0.5.3,<0.6.0',
 'numpy>=1.19.1,<2.0.0',
 'opencv-python>=4.4.0,<5.0.0']

entry_points = \
{'console_scripts': ['photoscanner = photoscanner.main:run']}

setup_kwargs = {
    'name': 'photoscanner',
    'version': '0.2.4',
    'description': 'A simple tool to digitalize printed photos using a greenscreen and a DSLR.',
    'long_description': '# PhotoScanner\nA simple tool to digitalize printed photos using a greenscreen and a DSLR.\n\n## Install\nThere are two ways to install the tool.\n\n### Pip\nRun `pip install photoscanner --user` to download and install.\n\n### From source\nInstall the poetry package manager and run the following commands.\n```\ngit clone git@github.com:Flova/PhotoScanner.git\ncd PhotoScanner\npoetry install\n```\n\n# Usage\nTo start the PhotoScanner run `photoscanner -h`.\n\nIf you installed PhotoScanner from source run `poetry run photoscanner -h`.\n\n# Setup\nThe setup should roughly look like this:\n\n![Photo Setup](https://github.com/Flova/PhotoScanner/raw/master/setup.jpg)\n\nA even lighting without reflections on the glossy surface of the photo results in the best quality. The printed image should be captured from the top on a green background.\n',
    'author': 'Florian Vahl',
    'author_email': 'florian@flova.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Flova/PhotoScanner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
