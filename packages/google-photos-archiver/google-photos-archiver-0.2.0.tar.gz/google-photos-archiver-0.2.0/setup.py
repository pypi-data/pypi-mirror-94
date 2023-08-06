# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['google_photos_archiver']

package_data = \
{'': ['*']}

install_requires = \
['click==7.1.2', 'google-auth-oauthlib>=0.4.2,<0.5.0', 'requests==2.25.1']

entry_points = \
{'console_scripts': ['google-photos-archiver = google_photos_archiver.cli:cli']}

setup_kwargs = {
    'name': 'google-photos-archiver',
    'version': '0.2.0',
    'description': 'Archives the contents of your Google Photos library to disk',
    'long_description': '# google-photos-archiver\n[![CircleCI](https://circleci.com/gh/scottx611x/google-photos-archiver.svg?style=svg&circle-token=54dbe16b5fd34bb8c3a646a479b75f640e1c18b5)](https://circleci.com/gh/scottx611x/google-photos-archiver/tree/main)\n[![codecov](https://codecov.io/gh/scottx611x/google-photos-archiver/branch/main/graph/badge.svg?token=KGmF8LIaY4)](https://codecov.io/gh/scottx611x/google-photos-archiver)\n[![PyPI version](https://badge.fury.io/py/google-photos-archiver.svg)](https://badge.fury.io/py/google-photos-archiver)\n\n* [What?](#what)\n* [Why?](#why)\n* [How?](#how)\n* [Development Pre\\-reqs](#development-pre-reqs)\n  * [Optional Reqs](#optional-reqs)\n* [Getting Started](#getting-started)\n  * [Google Oauth Setup](#google-oauth-setup)\n  * [First Run](#first-run)\n  * [Development Usage](#development-usage)\n  * [\\.\\.\\. with Docker](#-with-docker)\n  * [General Usage](#general-usage)\n  * [Running tests](#running-tests)\n* [Examples](#examples)\n  * [Specify a different download location](#specify-a-different-download-location)\n  * [Download from specific dates (with wildcard support)](#download-from-specific-dates-with-wildcard-support)\n  * [Download Albums and their MediaItems only](#download-albums-and-their-mediaitems-only)\n  * [Download Path Hierarchy](#download-path-hierarchy)\n\n[comment]: <> (Created with https://github.com/ekalinin/github-markdown-toc.go)\n[comment]: <> (brew install github-markdown-toc && cat ./README.md | gh-md-toc)\n\n## What?\n`google-photos-archiver` aims to provide a simple, fast, extensible interface to be able to back up one\'s Google Photos to a location of their choosing.\n\nI\'ve drawn inspiration from projects such as: https://github.com/mholt/timeliner & https://github.com/gilesknap/gphotos-sync but wanted to cut my teeth in this domain and see what I could come up with myself.\n\n## Why?\n\nI wanted a tool (of my own creation) which could easily provide a copy of mine and my partner\'s Google Photos libraries, and keep said copy up to date over time.\n\nIn reality I\'ve mainly just needed a distraction from the vicious cycle of wake, work, Netflix, sleep, and I thought it was high time to do a little side project.\n\n## How?\n\n### Development Pre-reqs\n\n- `docker`\n\n... Or\n\n- `python==3.8`\n- [poetry](https://python-poetry.org/docs/#installation) `>=1.0.0`\n\n#### Optional Reqs\n- [pre-commit](https://pre-commit.com/#install)\n  - Run `pre-commit install`\n\n### Getting Started\n\n#### Google Oauth Setup\nThese instructions will help you set up Google OAuth2 client credentials so you can start using `google-photos-archiver`\n\n- While logged into your Google account navigate to [Create a New Project](https://console.developers.google.com/projectcreate)\n- Create one, and switch to using it with the UI dropdown\n- Navigate to `APIs & Services` click on `+ Enable APIs and services`, and enable the `Photos Library API`\n- Navigate back to `APIs & Services` and click on `Credentials`\n- Click on `+ Create Credentials > OAuth client ID`\n- Configure an OAuth consent screen. You can just fill out the required fields and hit Save.\n  - Click `Add Or Remove Scopes` and manually add scope: `https://www.googleapis.com/auth/photoslibrary.readonly`\n  - Accept remaining defaults, save through and return to `Credentials`\n- Click on `+ Create Credentials > OAuth client ID`\n- Make a `"Desktop App"`\n- Congrats!, you now have a Client ID and Client Secret\n- Download the associated `client_secret.json` file and make note of its location as we\'ll be providing it\'s path to `google-photos-archiver`\n\n#### First Run\nA browser window will be opened during the initial OAuth flow. After successfully authenticating once, a refresh token will be stored for future use (See: `--refresh-token-path`) and will omit the need to reauthenticate.\n\n#### Development Usage\n```\n$ git clone git@github.com:scottx611x/google-photos-archiver.git\n$ poetry install\n$ poetry run google-photos-archiver --help\n```\n\n#### ... with Docker\n\n> Note that some more Docker volume mounting will be warranted here if you want to specify a different path to download to etc.\n> Ref: https://docs.docker.com/storage/volumes\n\n```\n$ docker build . -t google-photos-archiver\n$ docker run -v $PWD:/app/ google-photos-archiver  --help\n```\n\n#### General Usage\n\n```\n$ pip install google-photos-archiver\n$ google-photos-archiver --help\n```\n\n#### Running tests\n```\n$ poetry run pytest\n```\n\n### Examples\n\n#### Specify a different download location\n```\n$ google-photos-archiver archive-media-items --download-path /Volumes/my-big-hdd/downloaded_media\n```\n\n#### Download from specific dates (with wildcard support)\n```\n$ google-photos-archiver archive-media-items --date-filter 2020/*/*,2021/8/22\n$ google-photos-archiver archive-media-items --date-range-filter 2019/8/22-2020/8/22\n```\n\n#### Download Albums and their MediaItems only\n```\n$ google-photos-archiver archive-media-items --albums-only\n```\n\n#### Download Path Hierarchy\n```\n$ tree /<download_path>/downloaded_media/ | head\n/<download_path>/downloaded_media/\n├── 2021\n│ └── 1\n│     ├── 1\n│     │ └── a.jpg\n│     └── 2\n│         └── b.mov\n├── 2020\n│ ├── 1\n│ │ └── 2\n│ │     └── c.jpg\n│ └── 2\n│     └── 3\n│         └── d.jpg\n└── albums\n    └── Album A\n        └── <symlink /<download_path>/downloaded_media/2021/1/1/a.jpg >\n...\n```\n',
    'author': 'Scott Ouellette',
    'author_email': 'scottx611x@gmail.com',
    'maintainer': 'Scott Ouellette',
    'maintainer_email': 'scottx611x@gmail.com',
    'url': 'https://github.com/scottx611x/google-photos-archiver',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
