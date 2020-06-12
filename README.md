# githunt
### Browse most stared repositories by date on Github from your command line.
> This libray is inspired by the [Githunt](https://github.com/kamranahmedse/githunt) webapp created by [Kamran Ahmed](https://kamranahmed.info/), you can view it [here](https://kamranahmed.info/githunt/).


## Prerequisites
* Requires Python 3.7 or greater

## Installation
``` pip install githunt ```

## Usage
```
githunt --help

# Output
Usage: githunt [OPTIONS]

  Returns repositories based on the language. repositories are sorted by
  stars

Options:
  -l, --language TEXT  language filter (eg: python)
  -d, --date TEXT      date in the ISO8601 format which is YYYY-MM-DD (year-
                       month-day)
  -f, --fmt TEXT       output format, it can be either table or colored
  --help               Show this message and exit.

```