![Cover image](https://raw.githubusercontent.com/hedythedev/starcli/main/starcli-small-cover.png)

Browse trending projects on Github from your command line 💻


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
  -S, --spoken-language TEXT      Spoken Language filter eg: en for English,
                                  zh for Chinese, etc
  -c, --created TEXT              Specify repo creation date in YYYY-MM-DD,
                                  prefixing with >, <= etc is allowed
  -t, --topics TEXT               Search by topic. Can be specified multiple
                                  times. Multiple topics will be conjugated
                                  using &
  -u, --last-updated TEXT         Filter repos based on time of last update in
                                  ISO8601 format YYYY-MM-DD
  -L, --layout [list|table|grid]  The output format (list, table, or grid),
                                  default is list
  -s, --stars TEXT                Range of stars required, default is '>=100'
  -r, --limit-results INTEGER     Limit the number of results shown. Default:
                                  7
  -o, --order [desc|asc]          Specify the order of repos by stars that is
                                  shown, 'desc' or 'asc', default: desc
  --long-stats                    Print the actual stats[1300 instead of 1.3k]
  -d, --date-range [today|this-week|this-month]
                                  View stars received within time range,
                                  choose from: today, this-week, this-month
  -U, --user TEXT                 Search for trending repositories by username
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

### Filtering by spoken language

If you wanted to find repos in your native language, you can use `--spoken-language` or `-S`:

```
starcli --spoken-language zh
```

The above command lists down repos written in Chinese.
A full list of language codes is available [here](./starcli/spoken-languages.json)

Note that (like `--date-range`) options like `--topics`, `--last-updated`, `--created` won't take effect
because `-d` uses a different search mechanism to find results.

### Specify the number (or range) of stars

(Recommended to be used with `--created`)

The default range is >=100, you can change that!
Use `--stars` or `-s` to specify what you want,
for example, if you want to find repos that has more than 100 stars, you can use:

```
starcli -s '>100'
```

Note that if you do something like `>1000` not many repos can have
more than 1000 and is created within around 200 days,
to specify date of creation, use `--created`, see below.

### Filter by stars daily, weekly or monthly

Wish to know what's trending this week?!
You can view the number of stars a repo received today, this week or this month by using the `--date-range` or `-d` option:

```
starcli -d this-week -L table
```

This command will also display the number of stars received for each repo this week in the form of a table.

### Specify the date of creation

Want to find newer, older, or just created repos?
Just use `--created` or `-c`, and then
provide a date in ISO8601 format: yyyy-mm-dd

For example, for repos created on 1st January 2014, use:
```
starcli --created 2014-01-01
```

To search for repos that are created *on or after* 1st January 2014, use:
```
starcli --created '>=2014-01-01'
```

### Filtering by topics

This option helps you to filter by topics. You can use `--topics` or `-t` to include
a topic in search.
This option can be used multiple times.

```
starcli -l python -d 2020-07-06 -t deep-learning -t pytorch
```

### Specifying last updated date

Use this `--last-updated` or `-u` when you want to find popular repos that are
last updated on a given date, say 2020-01-01 for 1st of Jan
2020:

```
starcli -u 2020-01-01
```

### Searching by user

Recommended to be used with `--stars` and/or `--date-created`.

Finding trending projects by GitHub username is supported too. Use `--user` or `-U` to do so,
provide a valid GitHub username after that, like:

```
starcli -U hedythedev
starcli -U gvanrossum
```

### Using date ranges
You can use `--date-range` or `-d` and specify today, this-week, or this-month,
so that GitHub Trending search function will be used to find popular repos
and tell you how much stars are gained this day/week/month depending on the
option you used.

```
starcli -d this-week
```

<img src="https://raw.githubusercontent.com/hedythedev/starcli/main/demo-pics/daterange.png" width="800px;" alt="demo date range"/>

Note that (like `--spoken-language`) options like `--topics`, `--last-updated`, `--created` won't take effect
because `-d` uses a different search mechanism to find results.

### Limit the number of results shown
Don't like the default 7? You can change it to something else,
using `--limit-results` or `-r` followed by an integer:

```
starcli -r 2
```

The above will only give you two repos. This is useful if
you want to put it in your `.bashrc`, `.zshrc`, or `fish_greeting` function.

Just add `starcli -r 3 -L grid` in there, and every time you open your terminal,
you will find 3 trending repos printed neatly in a grid format, great way to start your
day (bit like the [Hacker Tab Extension](https://chrome.google.com/webstore/detail/hacker-tab/ibomigipadcieapbemkegkmadbbanbgm?hl=en) 😆 ).



## Issues, feature request, and feedback

* Issues, bug reports, or feature request: Don't hesitate to open an issue in this repo
* Feedback: any general feedback or questions about using StarCLI you can leave a comment 
on our [Product Hunt page](https://www.producthunt.com/posts/starcli), remember to be nice :)


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
    <td align="center"><a href="https://www.willmcgugan.com"><img src="https://avatars3.githubusercontent.com/u/554369?v=4" width="100px;" alt=""/><br /><sub><b>Will McGugan</b></sub></a><br /><a href="https://github.com/hedythedev/starcli/commits?author=willmcgugan" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/ashikjm"><img src="https://avatars1.githubusercontent.com/u/12744524?v=4" width="100px;" alt=""/><br /><sub><b>Ashik J M</b></sub></a><br /><a href="https://github.com/hedythedev/starcli/commits?author=ashikjm" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/ylchao"><img src="https://avatars0.githubusercontent.com/u/15059429?v=4" width="100px;" alt=""/><br /><sub><b>Yu-Lin Chao</b></sub></a><br /><a href="https://github.com/hedythedev/starcli/commits?author=ylchao" title="Code">💻</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/Saif807380"><img src="https://avatars2.githubusercontent.com/u/50794619?v=4" width="100px;" alt=""/><br /><sub><b>Saif Kazi</b></sub></a><br /><a href="https://github.com/hedythedev/starcli/commits?author=Saif807380" title="Code">💻</a> <a href="https://github.com/hedythedev/starcli/commits?author=Saif807380" title="Documentation">📖</a></td>
    <td align="center"><a href="http://arcanedomain.duckdns.org"><img src="https://avatars3.githubusercontent.com/u/16456078?v=4" width="100px;" alt=""/><br /><sub><b>arcanearronax</b></sub></a><br /><a href="https://github.com/hedythedev/starcli/commits?author=arcanearronax" title="Tests">⚠️</a> <a href="https://github.com/hedythedev/starcli/commits?author=arcanearronax" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!


## Credits

This project was forked from
[`githunt` (python)](https://github.com/SriNandan33/githunt)
and its initial intention was to rewrite that project to use
Rich instead of colorama + tabulate, but now it has so much more features
than before, thanks everyone!



---

Liked this project? Don't forget to give it a ⭐
