# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['autotrash']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['autotrash = autotrash.app:main']}

setup_kwargs = {
    'name': 'autotrash',
    'version': '0.4.2',
    'description': 'Script to automatically purge old trash',
    'long_description': 'Autotrash is a small python script to automatically remove\n(permanently delete) trashed files. It relies on the FreeDesktop.org\nTrash files for it\'s deletion information.\n\nIt scans the `~/.local/share/Trash/info` directory and reads the `.trashinfo`\nfiles to determine their deletion date. Files older then 30 days or files\nmatching a particular regular expression are then purged, including their\ntrash information file.\n\n![Travis CI build status](https://api.travis-ci.org/bneijt/autotrash.svg)\n\nInstallation\n============\n\nOn Fedora consider using `yum install autotrash`\n\n[On Ubuntu](https://packages.ubuntu.com/search?suite=all&arch=any&searchon=names&keywords=autotrash) and [Debian](https://packages.debian.org/search?keywords=autotrash&searchon=names&suite=stable&section=all) try to install it using `apt-get install autotrash`.\n\nArchLinux has an [AUR package available](https://aur.archlinux.org/packages/autotrash/). \n\nLast option is to install autotrash using pip, for example, using: `pip install --user autotrash`\n\n\nConfiguration\n=============\n\n## Automatic Setup ##\nrun `autotrash --install` to create a systemd service which runs daily with the provided arguments. For example\n\n    autotrash -d 30 --install\n\nwill run `/usr/bin/autotrash -d 30` daily.\n\nThe service can be manually started with `systemctl --user start autotrash`.\nThe timer can be enabled and disabled using `systemctl --user enable autotrash.timer` and\n`systemctl --user disable autotrash.timer` respectively.\n\nThe service is installed to `~/.config/systemd/user` so like the cron approach, root access is not required and multiple users have their own independent services.\n\n\n## Manual Cron Setup ##\nTo run autotrash daily using cron, add the following crontab entry:\n\n    @daily /usr/bin/autotrash -d 30\n\nYou can also make `autotrash` process all user trash directories (not just in your home directory) by adding this crontab entry:\n\n    @daily /usr/bin/autotrash -td 30\n\nOr more frequently, but to keep disk IO down, only when there is less then 3GB of free space:\n\n    @hourly /usr/bin/autotrash --max-free 3072 -d 30\n\nTo configure this, run "crontab -e" and add one of these lines in the\neditor, then save and close the file.\n\n\n## System Startup Setup ##\nIf you do not know how to work with crontab, you could add it to the startup\nprograms in GNOME using the menu: System -> Preferences -> Sessions\n\nAdd the program with the "+ Add" button.\n\nThis will make sure that your trash is cleaned up every time you log in.\n\n\nInformation\n===========\n\nHomepage: https://github.com/bneijt/autotrash\n\nAutotrash is now in the stable repo for Fedora 20 and is going to be synced out on the mirrors also for Fedora 21.\nEpel7 package is still in the testing repo but should go stable within few days.\n\nYou can install the package on Fedora right now with:\n\n    yum install autotrash\n\n\nDevelopment\n===========\n\nThe `autotrash` command is created as a script, using `poetry` you can run the current implementation using:\n\n    poetry run autotrash\n\nOr by using the shell:\n\n    poetry shell\n    autotrash --help\n\nAll pull requests and master builds are tested using github actions and require `black` formatting.\n',
    'author': 'A. Bram Neijt',
    'author_email': 'bram@neijt.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bneijt/autotrash',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
