![Cover image](https://github.com/hedythedev/starcli/blob/main/starcli-small-cover.png)
#### Browse trending repos on Github by :star:stars:star: from your command line :computer:
![Upload Python Package](https://github.com/hedythedev/starcli/workflows/Upload%20Python%20Package/badge.svg)
![Lint and test](https://github.com/hedythedev/starcli/workflows/Lint%20and%20test/badge.svg)



## Prerequisites
* Requires Python 3.7 or greater

## Installation
``` pip install starcli ```

## Usage
```
Usage: starcli [OPTIONS]

  Returns repositories based on the language. repositories are sorted by
  stars

Options:
  -l, --language TEXT  language filter (eg: python)
  -d, --date TEXT      date in the ISO8601 format which is YYYY-MM-DD (year-
                       month-day)
  -L, --layout TEXT       output format, it can be either table or list
  --help               Show this message and exit.
```

## Development
Make sure you read CONTRIBUTING.md first! 

**note: this proj is still in its early stage, if CONTRIBUTING.md is not yet created, create an issue to remind the maintainer!**

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
Start a pull request and wait for it to be reviewed!
