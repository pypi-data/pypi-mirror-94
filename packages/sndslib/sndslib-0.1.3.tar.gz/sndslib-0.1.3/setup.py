# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sndslib']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['snds = sndslib.cli:main']}

setup_kwargs = {
    'name': 'sndslib',
    'version': '0.1.3',
    'description': 'Process and verify data from SNDS easily',
    'long_description': "# SNDS LIB\n\n[![Build Status](https://www.travis-ci.com/undersfx/sndslib.svg?branch=master)](https://www.travis-ci.com/undersfx/sndslib) [![codecov](https://codecov.io/gh/undersfx/sndslib/branch/master/graph/badge.svg)](https://codecov.io/gh/undersfx/sndslib) [![Python 3](https://pyup.io/repos/github/undersfx/sndslib/python-3-shield.svg)](https://pyup.io/repos/github/undersfx/sndslib/) [![Updates](https://pyup.io/repos/github/undersfx/sndslib/shield.svg)](https://pyup.io/repos/github/undersfx/sndslib/)\n\nProcess and verify data from Microsoft's Smart Network Data Service (SNDS) API easily.\n\nSNDSLIB is a wrapper around SNDS Automated Data Access API to facilitate fast data process and analysis.\n\n---\n\n## What is SNDS?\n\nSmart Network Data Service (SNDS) is a platform to monitor data from IPs that send emails to Microsoft's servers.\n\nIf you send more than 100 messages per day from your IPs, your can get valuable information about IP reputation, possible blocks, spam complaints and spamtraps hits.\n\n---\n\n## Talk is cheap. Show me the code!\n\nInstallation:\n\nSNDSLIB has no external dependancies. It runs just with python 3.6 or higher.\n\n```bash\npip install sndslib\n```\n\nSimple example of library usage:\n\n```python\n    >>> from sndslib import sndslib\n\n    >>> r = sndslib.get_ip_status('mykey')\n    >>> blocked_ips = sndslib.list_blocked_ips(r)\n    >>> print(blocked_ips)\n    ['1.1.1.1', '1.1.1.2']\n\n    >>> list_blocked_ips_rdns(blocked_ips)\n    [{'ip': '1.1.1.1', 'rdns': 'foo.bar.exemple.com'},\n     {'ip': '1.1.1.2', 'rdns': 'foo2.bar.exemple.com'}]\n\n    >>> r = sndslib.get_data('mykey')\n    >>> sndslib.summarize(r)\n    {'red': 272, 'green': 710, 'yellow': 852, 'traps': 1298, 'ips': 1834, 'date': '12/31/2019'}\n\n    >>> sndslib.search_ip_status('1.1.1.1', r)\n    {'activity_end': '12/31/2019 7:00 PM',\n    'activity_start': '12/31/2019 10:00 AM',\n    'comments': '',\n    'complaint_rate': '< 0.1%',\n    'data_commands': '1894',\n    'filter_result': 'GREEN',\n    'ip_address': '1.1.1.1',\n    'message_recipients': '1894',\n    'rcpt_commands': '1895',\n    'sample_helo': '',\n    'sample_mailfrom': '',\n    'trap_message_end': '',\n    'trap_message_start': '',\n    'traphits': '0'}\n```\n\n---\n\n## CLI\n\nThis library contains a CLI to facilitate fast operations in the terminal. Here are some examples of their usage:\n\n### Summary of all IPs status\n```bash\nsnds -k 'your-key-here' -s\n```\nExample output:\n```\nDate: 12/31/2020\nIPs:       1915\nGreen:      250\nYellow:    1175\nRed:        490\nTrap Hits:  990\nBlocked:    193\n```\n\n### Individual report of a IP\n```bash\nsnds -k 'your-key-here' -ip '1.1.1.1'\n```\n\nExample output:\n```\nActivity: 1/31/2020 11:59 AM until 1/31/2020 11:59 PM\nIP:         1.1.1.1\nMessages:    183057\nFilter:       GREEN\nComplaint:   < 0.1%\nTrap Hits:        3\n```\n\n### List all IPs blocked\n```bash\nsnds -k 'your-key-here' -l\n```\n\nExample output:\n```\n1.1.1.1\n1.1.1.2\n1.1.1.3\n...\n```\n\n### List all IPs blocked with rDNS\n```bash\nsnds -k 'your-key-here' -r\n```\n\nExample output:\n```\n1.1.1.1;example.domain1.com\n1.1.1.2;example.domain2.com\n1.1.1.3;example.domain3.com\n...\n```\n\n---\n\nYou can get more information about SNDS features in the Microsoft's official pages for [SNDS](https://sendersupport.olc.protection.outlook.com/snds/FAQ.aspx?wa=wsignin1.0) and [SNDS Automated Data Access](https://sendersupport.olc.protection.outlook.com/snds/auto.aspx).\n",
    'author': 'undersfx',
    'author_email': 'undersoft.corp@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/undersfx/sndslib',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
