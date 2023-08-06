# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['epub2txt']

package_data = \
{'': ['*']}

install_requires = \
['ebooklib>=0.17.1,<0.18.0',
 'httpx>=0.16.1,<0.17.0',
 'logzero>=1.6.3,<2.0.0',
 'tqdm>=4.56.0,<5.0.0']

setup_kwargs = {
    'name': 'epub2txt',
    'version': '0.1.0',
    'description': 'Convert epub to txt with additonal utils',
    'long_description': '# epub2txt [![Codacy Badge](https://app.codacy.com/project/badge/Grade/0bef74fe4381412ab1172a06a93ad01e)](https://www.codacy.com/gh/ffreemt/epub2txt/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ffreemt/epub2txt&amp;utm_campaign=Badge_Grade)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\nConvert epub to txt with additonal utils\n\n<!--- Refer to dualtext-epub\\der_fanger_de_en.py\n\t\t__main__.py refer to tmx2epub.__main__\n--->\n\n## Installation\n\n```bash\npip install epub2txt\n# pip install epub2txt -U  # to upgrade\n```\n\n## Usage\n\n```python\nfrom epub2txt import epub2txt\n\n# from a url to epub\nurl = "https://github.com/ffreemt/tmx2epub/raw/master/tests/1.tmx.epub"\nres = epub2txt(url)\n\n# from a local epub file\nfilepath = r"tests\\test.epub"\nres = epub2txt(filepath)\n\n```',
    'author': 'freemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/epub2txt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
