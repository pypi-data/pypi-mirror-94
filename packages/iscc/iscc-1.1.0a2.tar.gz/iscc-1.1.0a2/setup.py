# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iscc']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8,<9',
 'PyLD>=2.0.3,<3.0.0',
 'av>=8.0,<9.0',
 'bech32>=1.2,<2.0',
 'bidict>=0.21.2,<0.22.0',
 'bitarray-hardbyte>=1.6,<2.0',
 'blake3>=0.1,<0.2',
 'codetiming>=1.2,<2.0',
 'humanize>=3.2,<4.0',
 'imageio-ffmpeg>=0.4,<0.5',
 'langcodes>=2.1,<3.0',
 'langdetect>=1.0,<2.0',
 'loguru>=0.5,<0.6',
 'more-itertools>=8.6,<9.0',
 'numpy<=1.19.3',
 'pydantic>=1.7,<2.0',
 'pyexiv2>=2.4,<3.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'requests>=2.25,<3.0',
 'scenedetect[opencv-headless]>=0.5,<0.6',
 'tika>=1.24,<2.0',
 'typer>=0.3.2,<0.4.0',
 'xxhash>=2,<3']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0'],
 ':sys_platform == "linux"': ['python-magic>=0.4.18,<0.5.0'],
 ':sys_platform == "win32" or sys_platform == "darwin"': ['python-magic-bin>=0.4.14,<0.5.0'],
 'turbo': ['cython>=0.29,<0.30'],
 'turbo:python_version >= "3.6" and python_version < "3.9"': ['numba==0.52']}

entry_points = \
{'console_scripts': ['igen = iscc.cli:app']}

setup_kwargs = {
    'name': 'iscc',
    'version': '1.1.0a2',
    'description': 'ISCC: Reference Implementation',
    'long_description': '# ISCC - Spec and Reference Code\n\n[![Build](https://travis-ci.org/iscc/iscc-specs.svg?branch=master)](https://travis-ci.org/iscc/iscc-specs)\n[![Version](https://img.shields.io/pypi/v/iscc.svg)](https://pypi.python.org/pypi/iscc/)\n[![License](https://img.shields.io/pypi/l/iscc.svg)](https://pypi.python.org/pypi/iscc/)\n[![Downloads](https://pepy.tech/badge/iscc)](https://pepy.tech/project/iscc)\n[![DOI](https://zenodo.org/badge/96668860.svg)](https://zenodo.org/badge/latestdoi/96668860)\n\nThe **International Standard Content Code** is a proposal for an [open standard](https://en.wikipedia.org/wiki/Open_standard) for decentralized content identification. This repository contains the specification of the proposed **ISCC Standard** and a reference implementation in Python3. The latest published version of the specification can be found at [iscc.codes](https://iscc.codes)\n\n| NOTE: This is ISCC Version 1.1 work in progress!!! |\n| --- |\n\n## Installing the reference code\n\nThe reference code is published with the package name [iscc](https://pypi.python.org/pypi/iscc) on Python Package Index. Install it with:\n\n``` bash\npip install iscc\n```\n\n## Using the reference code\n\nA short example on how to create an ISCC Code with the reference implementation.\n\n``` python\n>>> import iscc\n>>> iscc.code_iscc("README.md")\n{\n    \'characters\': 2918,\n    \'datahash\': \'d30edda59fd4803ad0d2754fcbda1ec4097d12bd790b10cd610a24764cfcef16\',\n    \'filename\': \'README.md\',\n    \'filesize\': 3075,\n    \'gmt\': \'text\',\n    \'iscc\': \'KADYHLZUJ43U3LX7C6P5LSJ7JHAETKCYHYCQ5YX4C3JQ5XNFT7KIAOQ\',\n    \'language\': \'en\',\n    \'mediatype\': \'text/markdown\',\n    \'metahash\': \'828dd01bf76b78fc448f6d2ab25008835d2993c6acde205235dc942083c4677d\',\n    \'title\': \'# ISCC Spec and Reference Code\'\n }\n```\n\n## Working with the specification\n\nThe entire **ISCC Specification** is written in plain text [Markdown](https://en.wikipedia.org/wiki/Markdown). The markdown content is than built and published with the excellent [mkdocs](http://www.mkdocs.org/) documetation tool. If you have some basic command line skills you can build and run the specification site on your own computer. Make sure you have the [git](https://git-scm.com/) and [Python](https://www.python.org/) and [Poetry](https://pypi.org/project/poetry/) installed on your system and follow these steps on the command line:\n\n``` bash\ngit clone https://github.com/iscc/iscc-specs.git\ncd iscc-specs\npoetry install\nmkdocs serve\n```\n\nAll specification documents can be found in the `./docs` subfolder or the repository. The recommended editor for the markdown files is [Typora](https://typora.io/). If you have commit rights to the [main repository](https://github.com/iscc/iscc-specs) you can deploy the site with a simple `mkdocs gh-deploy`.\n\n## Contribute\n\nPull requests and other contributions are welcome. Use the [Github Issues](https://github.com/iscc/iscc-specs/issues) section of this project to discuss ideas for the **ISCC Specification**. You may also want  join our developer chat on Telegram at <https://t.me/iscc_dev>.\n\n## License\n\nAll of documentation is licensed under the [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).\n\nReference code is licensed under BSD-2-Clause.\n',
    'author': 'Titusz Pan',
    'author_email': 'tp@py7.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://iscc.codes/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
