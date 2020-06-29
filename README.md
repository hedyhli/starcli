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

<br>

<!--Below is a demo gif-->
![starcli demo.gif](https://github.com/hedythedev/starcli/blob/main/demo.gif)




## Prerequisites

* Requires Python 3.6 or greater

## Installation

```sh
pip install starcli
```
*Remember to use `pip3` instead of `pip` if you also have Python 2 installed on your system*

## Usage

```sh
usage: starcli [-h] [-l LANG] [-d DATE] [-L {list,table}] [-s STARS] [-r LIMIT_RESULTS] [-o {desc,asc}] [--debug]

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
  -o {desc,asc}, --order {desc,asc}
                        Specify the order of repos by stars that is shown, 'desc' or 'asc', default: desc
  --debug               Turn on debugging mode
```

## Issues, feature request, and feedback

* Issues, bug reports, or feature request: Don't hesitate to open an issue in this repo
* Feedback: any general feedback or questions about using StarCLI you can leave a comment 
on our [Product Hunt page](https://www.producthunt.com/posts/starcli), remember to be nice :smiley:


## Development    [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

For contributing guidelines and how to set up your development environment, please 
read [`CONTRIBUTING.md`](https://github.com/hedythedev/starcli/blob/main/CONTRIBUTING.md).
Remember that all contributions to this project should follow its 
[CODE OF CONDUCT](https://github.com/hedythedev/starcli/blob/main/CODE_OF_CONDUCT.md).

## Uses

* CommandLine Argument parser: [`argparse`](https://github.com/python/cpython/blob/master/Lib/argparse.py)
(Planning to switch to `click`)
* Colored and table console print: [`rich`](https://github.com/willmcgugan/rich)
* HTTP library to send requests: [`requests`](https://github.com/psf/requests)


## Credits

This project was forked from
[`githunt` (python)](https://github.com/SriNandan33/githunt)
made by [Srinivasa Rao](https://github.com/SriNandan33), which
in turn, is inspired by
[`githunt` (the JavaScript Web App)](https://github.com/kamranahmedse/githunt).

