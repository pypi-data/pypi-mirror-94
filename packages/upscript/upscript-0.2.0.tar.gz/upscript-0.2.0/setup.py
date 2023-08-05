# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['upscript']

package_data = \
{'': ['*']}

install_requires = \
['distlib']

entry_points = \
{'console_scripts': ['upscript = upscript:main']}

setup_kwargs = {
    'name': 'upscript',
    'version': '0.2.0',
    'description': 'Installs and updates python scripts for you',
    'long_description': "Upscript\n===\n\nThis cli tool installs and updates python scripts for you.\n\nTested on: Linux, Windows.\n\nInstall\n---\n`pip install --user upscript`\n\nUsage\n---\n`upscript fetch <name> [<destination-dir>] [--index-url <index-url>]`\n\nThis command will create a folder with all the package's console entry points.\nThere also will be `.files/` folder inside it, containing embedded venv.\n\nAny time you'll start some of these entry point, upscript will check for a package update in an index. It is possible\nto suppress an update check via `UPSCRIPT_AUTO_UPDATE=0` env-var.\n",
    'author': 'xppt',
    'author_email': '21246102+xppt@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xppt/upscript',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
