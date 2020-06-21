![Cover image](https://github.com/hedythedev/starcli/blob/main/starcli-small-cover.png)
#### Browse trending repos on Github by :star:stars:star: from your command line :computer:
![checks](https://github.com/hedythedev/starcli/workflows/checks/badge.svg)
![pr checks](https://github.com/hedythedev/starcli/workflows/pr%20checks/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI version](https://badge.fury.io/py/starcli.svg)](https://badge.fury.io/py/starcli)
[![GitHub license](https://img.shields.io/github/license/hedythedev/starcli.svg)](https://github.com/hedythedev/starcli/blob/main/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)


## Prerequisites

* Requires Python 3.7 or greater

## Installation

```sh
pip install starcli
```

## Usage

```sh
Usage: starcli [OPTIONS]

  Returns repositories based on the language. repositories are sorted by
  stars

Options:
  -l, --language TEXT  language filter (eg: python)
  -d, --date TEXT      date in the ISO8601 format which is YYYY-MM-DD (year-
                       month-day)
  -L, --layout TEXT    output format, it can be either table or list
  -s, --stars TEXT     Specify the range of stars needed. Default: >=50
  --help               Show this message and exit.
```

## Development

Make sure you read CONTRIBUTING.md first!

First, fork this repo
then,

```sh
git clone https://github.com/{your_username}/starcli.git
cd starcli
python -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
git checkout -b your_br_name_here
```

Make the necessary changes, test your changes, then

```sh
git add .
git commit -m 'my commit message'
git push -u origin main
```

Start a pull request to the `develop` branch and wait for it to be reviewed!
