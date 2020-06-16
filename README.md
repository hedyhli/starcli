![Cover image](https://github.com/hedythedev/starcli/blob/main/starcli-small-cover.png)
#### Browse trending repos on Github by :star:stars:star: from your command line :computer:


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
  -f, --fmt TEXT       output format, it can be either table or colored
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
Make the neccessary changes, test your changes, then
```sh
git add .
git commit -m 'my commit message'
git push -u origin main
```
Start a pull request and wait for it to be reviewed!
