![Cover image](https://github.com/hedythedev/starcli/blob/main/starcli-small-cover.png)

*Browse trending repos on Github by*
⭐stars⭐ 
*from your command line!* 💻

![checks](https://github.com/hedythedev/starcli/workflows/checks/badge.svg)
![pr checks](https://github.com/hedythedev/starcli/workflows/pr%20checks/badge.svg)
[![pypi version](https://img.shields.io/pypi/v/starcli)](https://pypi.org/project/starcli/)
[![pypi downloads per month](https://img.shields.io/pypi/dm/starcli)](https://pypi.org/project/starcli/)
[![Python Requirements](https://img.shields.io/pypi/pyversions/starcli)](https://pypi.org/project/starcli/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub license MIT](https://img.shields.io/github/license/hedythedev/starcli.svg)](https://github.com/hedythedev/starcli/blob/main/LICENSE)


<!--Below is a demo gif-->
![starcli demo.gif](https://github.com/hedythedev/starcli/blob/main/demo.gif)


## Prerequisites

* Requires Python 3.6 or greater

## Installation

```sh
pip install starcli
```

## Usage

```sh
usage: starcli [-h] [-l LANG] [-d DATE] [-L {list,table}] [-s STARS] [-r LIMIT_RESULTS] [--debug]

Browse trending repos on GitHub by stars

optional arguments:
  -h, --help            show this help message and exit
  -l LANG, --lang LANG  Language filter eg:python
  -d DATE, --date DATE  Specify repo creation date in ISO8601 format YYYY-MM-DD
  -L {list,table}, --layout {list,table}
                        The output format (list or table), default is list
  -s STARS, --stars STARS
                        Range of stars required, default is '>=50'
  -r LIMIT_RESULTS, --limit-results LIMIT_RESULTS
                        Limit the number of results shown. Default: 7
  --debug               Turn on debugging mode
```

## Development

This project is still in its early development stage,
contributions are not suggested but issue reporting are welcome.
Once everything is stable, we will update this section and let your know how to contribute.
