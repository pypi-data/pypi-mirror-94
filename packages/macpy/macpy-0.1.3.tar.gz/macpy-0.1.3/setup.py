# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['macpy',
 'macpy.constant',
 'macpy.constant.XK',
 'macpy.interface',
 'macpy.libxkbswitch',
 'macpy.types']

package_data = \
{'': ['*']}

extras_require = \
{':sys_platform == "linux"': ['python-xlib>=0.26,<0.27',
                              'evdev>=1.3.0,<2.0.0',
                              'python-libinput>=0.1.0,<0.2.0']}

setup_kwargs = {
    'name': 'macpy',
    'version': '0.1.3',
    'description': 'Simple, cross-platform macros/GUI automation for python',
    'long_description': "macpy\n-----\n\n[mac]ro + [py]thon, pronounced like magpie.\n\n-------------------\n\nIf you find this software useful, `consider becoming a patron <https://www.patreon.com/ozymandias>`_\n\n-------------------\n\nThis package provides easy keyboard/pointer/window management macro creation\nand GUI automation for python versions 2.7 and 3.4+.\nCurrently it works on Windows and Linux (both under X and with limited\nfunctionality under Wayland).\nAmong it's features are:\n\n- Low level hooks for keyboard, pointer events\n- A hook for window creation, destruction and focus change\n- Support for registering hotkeys and hotstrings\n- Simulating keyboard/pointer events\n- Providing platform independent definition/mapping of keys/buttons\n- Listing open windows\n- Managing open windows\n- And more!\n\n.. Note::\n\n   Window management functionality is not available under Wayland.\n\n   More, keyboard and pointer functions require root access under Wayland.\n\n\nDocumentation\n~~~~~~~~~~~~~\n\nhttps://macpy.readthedocs.io/\n\nDevelopment\n~~~~~~~~~~~\n\nhttps://github.com/OzymandiasTheGreat/macpy\n\nPackage\n~~~~~~~\n\nhttps://pypi.org/project/macpy/\n",
    'author': 'Ozymandias',
    'author_email': 'tomas.rav@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/OzymandiasTheGreat/macpy',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
