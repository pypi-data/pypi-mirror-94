# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prettyqt',
 'prettyqt.__pyinstaller',
 'prettyqt.bluetooth',
 'prettyqt.charts',
 'prettyqt.constants',
 'prettyqt.core',
 'prettyqt.custom_animations',
 'prettyqt.custom_delegates',
 'prettyqt.custom_models',
 'prettyqt.custom_validators',
 'prettyqt.custom_widgets',
 'prettyqt.custom_widgets.regexeditor',
 'prettyqt.eventfilters',
 'prettyqt.gui',
 'prettyqt.iconprovider',
 'prettyqt.location',
 'prettyqt.multimedia',
 'prettyqt.multimediawidgets',
 'prettyqt.network',
 'prettyqt.objbrowser',
 'prettyqt.positioning',
 'prettyqt.prettyqtest',
 'prettyqt.qml',
 'prettyqt.qt',
 'prettyqt.qt.QtBluetooth',
 'prettyqt.qt.QtCharts',
 'prettyqt.qt.QtCore',
 'prettyqt.qt.QtGui',
 'prettyqt.qt.QtHelp',
 'prettyqt.qt.QtLocation',
 'prettyqt.qt.QtMultimedia',
 'prettyqt.qt.QtMultimediaWidgets',
 'prettyqt.qt.QtNetwork',
 'prettyqt.qt.QtPositioning',
 'prettyqt.qt.QtQml',
 'prettyqt.qt.QtQuick',
 'prettyqt.qt.QtSvg',
 'prettyqt.qt.QtTest',
 'prettyqt.qt.QtTextToSpeech',
 'prettyqt.qt.QtUiTools',
 'prettyqt.qt.QtWebChannel',
 'prettyqt.qt.QtWebEngineCore',
 'prettyqt.qt.QtWebEngineWidgets',
 'prettyqt.qt.QtWidgets',
 'prettyqt.qt.QtWinExtras',
 'prettyqt.qthelp',
 'prettyqt.quick',
 'prettyqt.scintilla',
 'prettyqt.svg',
 'prettyqt.syntaxhighlighters',
 'prettyqt.syntaxhighlighters.pygments',
 'prettyqt.texttospeech',
 'prettyqt.utils',
 'prettyqt.webchannel',
 'prettyqt.webenginecore',
 'prettyqt.webenginewidgets',
 'prettyqt.widgets',
 'prettyqt.winextras']

package_data = \
{'': ['*'],
 'prettyqt': ['localization/*', 'themes/*'],
 'prettyqt.iconprovider': ['fonts/*']}

install_requires = \
['bidict>=0,<1',
 'deprecated>=1.2.10,<2.0.0',
 'orjson>=3.2.0,<4.0.0',
 'pygments>=2.6.1,<3.0.0',
 'qstylizer>=0.1.9,<0.2.0',
 'regex>=2020.6.8,<2021.0.0']

extras_require = \
{':sys_platform == "darwin"': ['darkdetect>=0,<1'],
 ':sys_platform == "win32"': ['pywin32>=300,<301'],
 'addons': ['docutils>=0,<1'],
 'pyqt5': ['PyQt5>=5.15.0,<6.0.0',
           'PyQtWebEngine>=5.15.0,<6.0.0',
           'PyQtChart>=5.15.0,<6.0.0',
           'QScintilla>=2.11.5,<3.0.0'],
 'pyqt6': ['PyQt6>=6.0.0,<7.0.0'],
 'pyside2:python_version < "3.10"': ['pyside2>=5.15.0,<6.0.0'],
 'pyside6:python_version < "3.10"': ['pyside6>=6.0.0,<7.0.0']}

entry_points = \
{'console_scripts': ['iconbrowser = prettyqt.custom_widgets.iconbrowser:run',
                     'regexeditor = '
                     'prettyqt.custom_widgets.regexeditor.__main__:run'],
 'pyinstaller40': ['hook-dirs = prettyqt.__pyinstaller:get_hook_dirs'],
 'pytest11': ['pytest-qt = prettyqt.prettyqtest.plugin']}

setup_kwargs = {
    'name': 'prettyqt',
    'version': '0.183.2',
    'description': 'A pythonic layer on top of PyQt5 / PySide2 / PySide6',
    'long_description': '# prettyqt: Pythonic layer on top of PyQt5 / PySide2 / PySide6\n[![PyPI Latest Release](https://img.shields.io/pypi/v/prettyqt.svg)](https://pypi.org/project/prettyqt/)\n[![Package Status](https://img.shields.io/pypi/status/prettyqt.svg)](https://pypi.org/project/prettyqt/)\n[![License](https://img.shields.io/pypi/l/prettyqt.svg)](https://github.com/phil65/PrettyQt/blob/master/LICENSE)\n[![Travis Build Status](https://travis-ci.org/phil65/prettyqt.svg?branch=master)](https://travis-ci.org/phil65/prettyqt)\n[![CodeCov](https://codecov.io/gh/phil65/PrettyQt/branch/master/graph/badge.svg)](https://codecov.io/gh/phil65/PrettyQt)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![PyUp](https://pyup.io/repos/github/phil65/PrettyQt/shield.svg)](https://pyup.io/repos/github/phil65/PrettyQt/)\n\n## What is it?\n\n**PrettyQt** is a Python package that provides a pythonic layer on top of the GUI frameworks PyQt5 / PySide2 / PySide6.\n\n## Main Features\nHere are just a few of the things that PrettyQt does well:\n\n  - Large parts of the Qt API are available in a **PEP-8**-compliant way.\n  - Several predefined widgets, validators, models, syntax highlighters are included.\n  - A regex module based on QRegularExpression with the same API as Pythons core re module.\n\n\n   [widgets]: https://phil65.github.io/PrettyQt/widgets.html\n   [validators]: https://phil65.github.io/PrettyQt/validators.html\n   [syntaxhighlighters]: https://phil65.github.io/PrettyQt/syntaxhighlighters.html\n   [models]: https://phil65.github.io/PrettyQt/models.html\n\n\n## Where to get it\nThe source code is currently hosted on GitHub at:\nhttps://github.com/phil65/PrettyQt\n\nThe latest released version are available at the [Python\npackage index](https://pypi.org/project/prettyqt).\n\n```sh\n# or PyPI\npip install prettyqt\n```\n\n## Dependencies\n- [bidict](https://pypi.org/project/bidict)\n- [orjson](https://pypi.org/project/orjson)\n- [regex](https://pypi.org/project/regex)\n- [docutils](https://pypi.org/project/docutils)\n\n\n## Installation from sources\n\nThis project uses poetry for dependency management and packaging. Install this first.\nIn the `prettyqt` directory (same one where you found this file after\ncloning the git repo), execute:\n\n```sh\npoetry install\n```\n\n## License\n[MIT](LICENSE)\n\n## Documentation\nThe official documentation is hosted on Github Pages: https://phil65.github.io/PrettyQt/\n\n## Contributing to prettyqt [![Open Source Helpers](https://www.codetriage.com/phil65/prettyqt/badges/users.svg)](https://www.codetriage.com/phil65/prettyqt)\n\nAll contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.\n\nOr maybe through using PrettyQt you have an idea of your own or are looking for something in the documentation and thinking ‘this can be improved’...you can do something about it!\n',
    'author': 'phil65',
    'author_email': 'philipptemminghoff@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/phil65/prettyqt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
