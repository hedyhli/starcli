![Cover image](https://raw.githubusercontent.com/hedythedev/starcli/main/starcli-small-cover.png)

*Browse trending repos on Github by*
⭐stars⭐
*from your command line!* 💻


![checks](https://github.com/hedythedev/starcli/workflows/checks/badge.svg)
[![pypi version](https://img.shields.io/pypi/v/starcli)](https://pypi.org/project/starcli/)
[![pypi downloads per month](https://img.shields.io/pypi/dm/starcli)](https://pypi.org/project/starcli/)
[![Python Requirements](https://img.shields.io/pypi/pyversions/starcli)](https://pypi.org/project/starcli/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub license MIT](https://img.shields.io/github/license/hedythedev/starcli.svg)](https://github.com/hedythedev/starcli/blob/main/LICENSE)

<br>

<!--Below is a demo gif-->
![starcli demo.gif](https://raw.githubusercontent.com/hedythedev/starcli/main/starcli-demo2.gif)





## Prerequisites

* Requires Python 3.6 or greater

## Installation

```sh
pip install starcli
```
*Remember to use `pip3` instead of `pip` if you also have Python 2 installed on your system*


## Usage

```sh
Usage: starcli [OPTIONS]

  Browse trending repos on GitHub by stars

Options:
  -l, --lang TEXT                 Language filter eg: python
  -d, --date TEXT                 Specify repo creation date in ISO8601 format
                                  YYYY-MM-DD
  -L, --layout [list|table|grid]  The output format (list, table, or grid),
                                  default is list
  -s, --stars TEXT                Range of stars required, default is '>=50'
  -r, --limit-results INTEGER     Limit the number of results shown. Default:
                                  7
  -o, --order [desc|asc]          Specify the order of repos by stars that is
                                  shown, 'desc' or 'asc', default: desc
  --long-stats                    Print the actual stats[1300 instead of 1.3k]
  --debug                         Turn on debugging mode
  --help                          Show this message and exit.
```


### Layouts

Switch layouts using `--layout {list|table|grid}`, or use the short option `-L`

**list**

<img src="https://raw.githubusercontent.com/hedythedev/starcli/main/demo-pics/list.png" width="400px;" alt="demo list"/> 

**table**

<img src="https://raw.githubusercontent.com/hedythedev/starcli/main/demo-pics/table.png" width="800px;" alt=""/>

**grid**

<img src="https://raw.githubusercontent.com/hedythedev/starcli/main/demo-pics/grid.png" width="800px;" alt="demo grid"/>


### Filtering by language

For example, you only want to find popular Python repos, you can use `--lang` or `-l`:

```
starcli --lang python
```

Here, we used `starcli -l python -L grid`, which is python with grid layout:

<img src="https://raw.githubusercontent.com/hedythedev/starcli/main/demo-pics/lang.png" width="800px;" alt="demo grid"/>


### Specify the number (or range) of stars

(Recommended to be used with `--date`)

The default range is >=50, you can change that! Use `--stars` or `-s` to specify what you want,
for example, if you want to find repos that has more than 100 stars, you can use:

```
starcli -s '>100'
```

Note that if you do something like `>1000` not many repos can have
more than 1000 and is created within 100 days, to specify date of creation, use `--date`, see below.

### Specify the date of creation

Want to find newer, older, or just created repos? Just use `--date` or `-d`, and then
provide a date in ISO8601 format: yyyy-mm-dd

For example, to 1st January 2014, use:
```
starcli --date 2014-01-01
```

### Limit the number of results shown
Don't like the default 7? You can change it to something else,
using `--limit-results` or `-r` followed by an integer:

```
starcli -r 2
```

The above will only give you two repos. This is useful if
you want to put it in your `.bashrc`, `.zshrc`, or `config.fish`.

Just add `starcli -r 3 -L grid` to that file, and every time you open your terminal,
you will find 3 trending repos printed neatly in a grid format, great way to start your
day (bit like the [Hacker Tab Extension](https://chrome.google.com/webstore/detail/hacker-tab/ibomigipadcieapbemkegkmadbbanbgm?hl=en) 😆 ).



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

* CommandLine Argument parser: [Click](https://github.com/pallets/click)
* Colored and table console print: [`rich`](https://github.com/willmcgugan/rich) (with click and colorama)
* HTTP library to send requests: [`requests`](https://github.com/psf/requests)



## Contributors ✨

Thanks goes to all of these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/Shagilton"><img src="https://avatars0.githubusercontent.com/u/21122143?v=4" width="100px;" alt=""/><br /><sub><b>Shagilton</b></sub></a><br /><a href="https://github.com/hedythedev/starcli/commits?author=Shagilton" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/hexbee"><img src="https://avatars2.githubusercontent.com/u/26668583?v=4" width="100px;" alt=""/><br /><sub><b>hexbee</b></sub></a><br /><a href="https://github.com/hedythedev/starcli/issues?q=author%3Ahexbee" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/swellander"><img src="https://avatars0.githubusercontent.com/u/22231097?v=4" width="100px;" alt=""/><br /><sub><b>Sam Wellander</b></sub></a><br /><a href="https://github.com/hedythedev/starcli/commits?author=swellander" title="Code">💻</a></td>
    <td align="center"><a href="https://www.shivamsinha.xyz/"><img src="https://avatars0.githubusercontent.com/u/32016929?v=4" width="100px;" alt=""/><br /><sub><b>Shivam Sinha</b></sub></a><br /><a href="https://github.com/hedythedev/starcli/commits?author=shivam212" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!


## Credits

This project was forked from
[`githunt` (python)](https://github.com/SriNandan33/githunt)
made by [Srinivasa Rao](https://github.com/SriNandan33), which
in turn, is inspired by
[`githunt` (the JavaScript Web App)](https://github.com/kamranahmedse/githunt).



---

Liked this project? Don't forget to give it a ⭐
