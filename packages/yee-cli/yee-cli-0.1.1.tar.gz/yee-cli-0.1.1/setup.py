# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['yee']

package_data = \
{'': ['*']}

install_requires = \
['Click>=7.0,<8.0', 'webcolors>=1.11.1,<2.0.0', 'yeelight>=0.5.4,<0.6.0']

entry_points = \
{'console_scripts': ['yee = yee.cli:main']}

setup_kwargs = {
    'name': 'yee-cli',
    'version': '0.1.1',
    'description': 'Simple Yeelight Room control CLI written in Python.',
    'long_description': '=======\nYee CLI\n=======\n.. image:: https://brands.home-assistant.io/_/yeelight/logo.png\n\n.. image:: https://img.shields.io/pypi/v/yee-cli.svg\n        :target: https://pypi.python.org/pypi/yee-cli\n\n.. image:: https://github.com/adamwojt/yee-cli/workflows/ci/badge.svg?branch=master&event=push\n        :target: https://github.com/adamwojt/yee-cli/actions\n\n.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336\n        :target: https://timothycrosley.github.io/isort/\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n        :target: https://github.com/psf/black\n\n\nSimple Yeelight Room control CLI written in Python.\n\nInstallation\n------------\n\n.. code-block:: text\n\n    pip install yee-cli\n    \n\nConfig\n------\n\n* Location: ``~/.yee_rooms``\n* Format: ``JSON``\n* Example:\n\n.. code-block:: json\n\n    {\n       "office":[\n          "192.168.1.1",\n          "192.168.1.2"\n       ],\n       "bedroom":[\n          "192.168.1.3",\n          "192.168.1.4"\n       ]\n    }\n\n* Config path can be also passed with ``-c`` flag or ``YEE_ROOM_CONFIG`` env variable\n* To find bulb IPs use tools like ``nmap``, ``putty`` or check on your `YeeLight app <https://play.google.com/store/apps/details?id=com.yeelight.cherry&hl=en&gl=US>`_\n\nUsage\n-----\n``yee [-c --config] [ROOM_NAME*] COMMAND [ARGS]...```\n\n*\\*Use room names from config*\n\n**Example Usage:**\n\n.. code-block:: text\n\n    yee bedroom on\n    yee office dim 10\n    yee color_list\n    yee office color indianred\n    ... romance on !\n\n**Commands:**\n\n.. code-block:: text\n\n    color         Set lights to given color.\n    color_list    Available color list\n    dim           Dim lights to level (1-100).\n    off           Turn lights off.\n    on            Turn lights on.\n    random_color  Switch to random color.\n    toggle        Toggle lights.\n\n\nTroubleshooting\n---------------\n\nConnection Issues (make sure):\n    * IP addresses of bulbs in config are correct.\n    * LAN Control is ON (https://www.yeelight.com/faqs/lan_control).\n    * You are connected to same WIFI network as your bulbs.\nOther:\n    * For more debug ideas visit https://github.com/skorokithakis/python-yeelight\n\nCredits\n-------\n\n* Wouldn\'t be possible without `skorokithakis/python-yeelight <https://github.com/skorokithakis/python-yeelight>`_.\n* Uses `webcolors <https://pypi.org/project/webcolors/>`_\n* Uses `click <https://click.palletsprojects.com/en/7.x/>`_\n* Created with Cookiecutter_ and the `johanvergeer/cookiecutter-poetry`_ project template.\n\nAfter writing almost all I realised that author of `python-yeelight <https://github.com/skorokithakis/python-yeelight>`_ also wrote CLI. Check it out - it has different API / config and more features >>> `yeecli <https://github.com/skorokithakis/yeecli>`_\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`johanvergeer/cookiecutter-poetry`: https://github.com/johanvergeer/cookiecutter-poetry\n',
    'author': 'Adam Wojtczak',
    'author_email': 'adam1edinburgh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adamwojt/yee-cli',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
