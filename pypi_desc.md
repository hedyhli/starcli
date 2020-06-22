# StarCLI

Browse trending repos on Github by stars from your command line!

## Prerequisites

* Requires Python 3.7 or greater

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

### For a more detailed readme and documentation

please read [README.md in the GitHub repo](https://github.com/hedythedev/starcli).

