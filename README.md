![Cover image](https://github.com/hedythedev/starcli/blob/main/starcli-small-cover.png)

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
![starcli demo.gif](https://github.com/hedythedev/starcli/blob/main/starcli-demo2.gif)




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
  -l, --lang TEXT              Language filter eg: python
  -d, --date TEXT              Specify repo creation date in ISO8601 format
                               YYYY-MM-DD
  -L, --layout [list|table|grid]  The output format (list, table, or grid),
                                  default is list
  -s, --stars TEXT             Range of stars required, default is '>=50'
  -r, --limit-results INTEGER  Limit the number of results shown. Default: 7
  -o, --order [desc|asc]       Specify the order of repos by stars that is
                               shown, 'desc' or 'asc', default: desc
  --debug                      Turn on debugging mode
  --help                       Show this message and exit.
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

* CommandLine Argument parser: [Click](https://github.com/pallets/click)
* Colored and table console print: [`rich`](https://github.com/willmcgugan/rich)
* HTTP library to send requests: [`requests`](https://github.com/psf/requests)





## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/Shagilton"><img src="https://avatars0.githubusercontent.com/u/21122143?v=4" width="100px;" alt=""/><br /><sub><b>Shagilton</b></sub></a><br /><a href="https://github.com/hedythedev/starcli/commits?author=Shagilton" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/hexbee"><img src="https://avatars2.githubusercontent.com/u/26668583?v=4" width="100px;" alt=""/><br /><sub><b>hexbee</b></sub></a><br /><a href="https://github.com/hedythedev/starcli/issues?q=author%3Ahexbee" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/swellander"><img src="https://avatars0.githubusercontent.com/u/22231097?v=4" width="100px;" alt=""/><br /><sub><b>Sam Wellander</b></sub></a><br /><a href="https://github.com/hedythedev/starcli/commits?author=swellander" title="Code">💻</a></td>
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
