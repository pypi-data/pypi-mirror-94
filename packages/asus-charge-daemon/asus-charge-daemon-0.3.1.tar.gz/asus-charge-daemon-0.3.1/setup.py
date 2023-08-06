# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asuscharged']

package_data = \
{'': ['*']}

install_requires = \
['PyGObject>=3.38.0,<4.0.0',
 'asus-charge-control>=1.0.3,<2.0.0',
 'asyncinotify>=2.0.2,<3.0.0',
 'dbus-next>=0.2.2,<0.3.0']

entry_points = \
{'console_scripts': ['asuscharged = asuscharged.__main__:main']}

setup_kwargs = {
    'name': 'asus-charge-daemon',
    'version': '0.3.1',
    'description': 'A daemon exposing D-Bus services for managing the charge level of recent ASUS notebooks.',
    'long_description': "# asus-charge-daemon\n\n> A daemon exposing D-Bus services for managing the charge level of recent\nASUS notebooks.\n\nRecent ASUS notebooks come with a Windows application to set the maximum battery\ncharge level, in order to reduce stress on the battery and prolong its lifespan. On\nLinux kernels >= version 5.4, the ```asus_nb_wmi``` kernel module exposes a sysfs object to manage this setting.\n\n```asus-charge-daemon``` is a system service that runs in the background, exposing a D-Bus interface on the System Bus, enabling userspace applications to manage the maximum battery charge level.\n\n## Installation\n\nasus-charge-daemon should work with any device running a recent kernel (>= 5.4) with the ```asus_nb_wmi``` module loaded. Use ```lsmod | grep asus_nb_wmi``` to check; if you see a line like ```asus_nb_wmi            32768  0```, then the module is running.\n\nIt has been tested with the following ASUS notebooks:\n\n- ASUS VivoBook 15 **X512DA**\n\nA Python version >= 3.7 is necessary to run this daemon. Most Linux distributions come with the right version. To verify that Python is installed on **Debian**/**Ubuntu**-based distributions, use ```apt```:\n\n```console\nsudo apt install python3\n```\n\nOn **Arch**-based distributions, use ```pacman```:\n\n```console\nsudo pacman -Syu python\n```\n\nOn **RHEL/Fedora**-based distributions, use ```rpm```:\n\n```console\nsudo rpm -i python3\n```\n\n### Manual\n\nA **very** rudimentary installation script is included for easy installation. It will copy the files to the appropriate places, install the Python modules, and run the system service.\n\nDownload and run the installation script:\n\n```console\ncurl https://raw.githubusercontent.com/cforrester1988/asus-charge-daemon/main/install.py -o install.py\nchmod +x install.py\nsudo ./install.py install\n```\n\nTo update, run the installation script again, as above. To uninstall:\n\n```console\nsudo ./install.py uninstall\n```\n\n#### git version\n\nClone the git repository locally:\n\n```console\n$ git clone https://github.com/cforrester1988/asus-charge-daemon.git\nCloning into 'asus-charge-daemon'...\n```\n\nNavigate to the directory you cloned the repository into, and run the installation script. Append ```local``` to work with the cloned package, instead of downloading it from PyPI.\n\n```console\ncd asus-charge-daemon\nsudo ./install.py install local\n```\n\nTo update, pull the latest changes and reinstall:\n\n```console\ngit pull\nsudo ./install.py reinstall local\n```\n\nTo uninstall, run the installation script again:\n\n```console\nsudo ./install.py uninstall\n```\n\n## Version history\n\n- 0.3.0 (2021-02-07)\n  - (feature) Desktop notifications\n  - (feature) Monitor threshold for outside changes\n  - (feature) Monitor config for changes\n\n- 0.2.0 (2021-01-23)\n  - Initial public release.\n",
    'author': 'Christopher Forrester',
    'author_email': 'christopher@cforrester.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com./cforrester1988/asus-charge-daemon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
