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
usage: starcli [-h] [-l LANG] [-d DATE] [-L {list,table}] [-s STARS] [--debug]

Browse trending repos on GitHub by stars

optional arguments:
  -h, --help            show this help message and exit
  -l LANG, --lang LANG  Language filter eg:python
  -d DATE, --date DATE  Specify repo creation date in ISO8601 format YYYY-MM-DD
  -L {list,table}, --layout {list,table}
                        The output format (list or table), default is list
  -s STARS, --stars STARS
                        Range of stars required, default is '>=50'
  --debug               Turn on debugging mode
```

## Development

This project is still in its early development stage, contributions are not suggested but issue reporting are welcome. 
Once everything is stable, we will update this section and let your know how to contribute.
