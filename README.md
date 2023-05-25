```
  ___  ______    _     ____     ____   _     _
 / \ *   | |    /\    | |  \   / |  * | \   | \
 \  \    | |   /\ \   | |* /  |  |    | |   | |
  \  \   | |  /--\ \  | | \   |  |    | |   | |
 *_\./   ._| /    ._\ |_|  \_  \.|__. |_|_. |_|

```

Browse trending projects on Github from your command line `$ _`


![checks](https://github.com/hedyhli/starcli/workflows/checks/badge.svg)
[![pypi version](https://img.shields.io/pypi/v/starcli)](https://pypi.org/project/starcli/)
[![pypi downloads per month](https://img.shields.io/pypi/dm/starcli)](https://pypi.org/project/starcli/)
[![Python Requirements](https://img.shields.io/pypi/pyversions/starcli)](https://pypi.org/project/starcli/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub license MIT](https://img.shields.io/github/license/hedyhli/starcli.svg)](https://github.com/hedyhli/starcli/blob/main/LICENSE)

<br>

<!--Below is a demo gif-->
![starcli demo.gif](https://raw.githubusercontent.com/hedyhli/starcli/main/images/starcli-demo2.gif)

## Features

* Filters
  * Stars
  * Pushed date
  * Created date
  * User
  * Topic
  * Language
  * Spoken language
* Use generic GitHub search API or GitHub trending
* Auth token (optional)
* Paged output
* Different layouts


## Prerequisites

* Requires Python 3.6 or greater

## Installation

```sh
pip3 install starcli
```

## Usage

```
Usage: starcli [OPTIONS]

  Search and query GitHub repositories

Options:
  -l, --lang TEXT                 Language filter eg: python. (can be used
                                  multiple times)
  -S, --spoken-language TEXT      Spoken Language filter eg: en for English,
                                  zh for Chinese
  -c, --created TEXT              Specify repo creation date in YYYY-MM-DD,
                                  use >date, <=date etc to be more specific.
  -t, --topic TEXT                Date of last push in YYYY-MM-DD (>, <, >=,
                                  <= specifiers supported)
  -p, --pushed TEXT               Specify date of last push in YYYY-MM-DD, >=<
                                  allowed
  -L, --layout [list|table|grid]  The output format (list, table, or grid),
                                  default is list
  -s, --stars TEXT                Number of stars, default is '>=100'. eg:
                                  '>0', '123', '<50000
  -n, --num-results INTEGER       The number of items in the results. Default:
                                  7
  -o, --order [desc|asc]          Order of repos by stars, 'desc' or 'asc',
                                  default: desc
  --long-stats                    Print the actual stats number (1300 instead
                                  of 1.3k)
  -d, --date-range [day|week|month]
                                  View stars received within time, choose
                                  from: day, week, month. Uses GitHub trending
                                  for fetching results, hence some other
                                  filter options may not work.
  -u, --user TEXT                 Filter for trending repositories by username
  --auth TEXT                     Optionally use GitHub personal access token
                                  in the format 'username:password'.
  -P, --pager                     Use $PAGER to page output. (put -r in $LESS
                                  to enable ANSI styles)
  --debug                         Turn on debugging mode
  --help                          Show this message and exit.
```


### Layouts

Switch layouts using `--layout {list|table|grid}`, or use the short option `-L`

**list**

<img src="https://raw.githubusercontent.com/hedyhli/starcli/main/images/list.png" width="400px;" alt="demo list"/>

**table**

<img src="https://raw.githubusercontent.com/hedyhli/starcli/main/images/table.png" width="800px;" alt=""/>

**grid**

<img src="https://raw.githubusercontent.com/hedyhli/starcli/main/images/grid.png" width="800px;" alt="demo grid"/>

All three of the layout options support clickable links for repository names. If
your terminal supports links, you can directly click on the name and it will
take you to the GitHub repository in your browser.


### Filtering by language

For example, you only want to find popular Python repos: using `--lang` or `-l`:

```
starcli --lang python
```

Here's another example `starcli -l python -L grid`, which is python with grid
layout:

<img src="https://raw.githubusercontent.com/hedyhli/starcli/main/images/lang.png" width="800px;" alt="demo grid"/>

### Filtering by spoken language

If you wanted to find repos in your native language, you can use
`--spoken-language` or `-S`:

```
starcli --spoken-language zh
```

The above command lists down repos written in Chinese.

A full list of language codes is available
[here](./starcli/spoken-languages.json)

Note that (as with `--date-range`) options like `--topics`, `--pushed`,
`--created` won't take effect because `-d` uses a different search mechanism to
find results.

### Specify the number (or range) of stars

(Recommended to be used with `--created`)

The default range is >=100 stars.

Use `--stars` or `-s` to specify what you want, for example, if you want to find
repos that has more than 100 stars, you can use:

```
starcli -s '>100'
```

Note that if you do something like `>1000` not many repos can have more than
1000 and is created within around 200 days (which is the default for
`--created`), to specify date of creation, use `--created`, see below.

### Filter by stars daily, weekly or monthly

You can view the number of stars a repo received today, this week or this month
by using the `--date-range` or `-d` option:

```
starcli -d this-week -L table
```

This command will also display the number of stars received for each repo this
week in the form of a table.

`-d` uses GitHub Trending search for repositories, hence options `--topic`,
`--pushed`, `--created` won't take effect.

### Specify the date of creation

`--created`/`-c` accepts a date in ISO8601 format: yyyy-mm-dd

For example, for repos created on 1st January 2014, use:
```
starcli --created 2014-01-01
```

To search for repos that are created *on or after* 1st January 2014, use:
```
starcli --created '>=2014-01-01'
```

### Filtering by topics

This option lets you filter by topics. You can use `--topics` or `-t` to include
a topic in search.

This option can be used multiple times.

```
starcli -l python -d 2020-07-06 -t deep-learning -t pytorch
```

### Specifying last pushed date

Use `--pushed`/`-p` when you want to find popular repos that are last updated on
a given date, say 2020-01-01 for 1st of Jan 2020:

```
starcli -p 2020-01-01
```

You can also prefix the value with ">=<" like:

```
starcli -p '>=2020-01-01'
```

This is find repos that have last pushed after or on January the 1st, 2020.

Read more about the >=< syntax on [GitHub
Docs](https://docs.github.com/en/github/searching-for-information-on-github/understanding-the-search-syntax#query-for-values-greater-or-less-than-another-value).

### Searching by user

Recommended to be used with `--stars` and/or `--date-created`.

Finding trending projects by GitHub username is supported too. Use `--user` or
`-u` to do so.

Just provide a valid GitHub username after it, like:

```
starcli -u torvalds
starcli -u gvanrossum
```

### Using date ranges

You can use `--date-range` or `-d` and specify today, this-week, or this-month,
so that GitHub Trending search function will be used to find popular repos and
tell you how much stars are gained this day/week/month depending on the option
you used.

```
starcli -d this-week
```

<img src="https://raw.githubusercontent.com/hedyhli/starcli/main/images/daterange.png" width="800px;" alt="demo date range"/>

Note that (like `--spoken-language`) options like `--topics`, `--pushed`,
`--created` won't take effect because `-d` uses a different search mechanism to
find results.

### Limit the number of results shown

Don't like the default 7? You can change it to something else, using
`--limit-results` or `-r` followed by an integer:

```
starcli -r 2
```

The above will only give you two repos. This is useful if you want to put it in
your `.bashrc`, `.zshrc`, or `fish_greeting` function.

Just add `starcli -r 3 -L grid` in there, and every time you open your terminal,
you will find 3 trending repos printed neatly in a grid format, great way to
start your day (a bit like the [Hacker Tab
Extension](https://chrome.google.com/webstore/detail/hacker-tab/ibomigipadcieapbemkegkmadbbanbgm?hl=en)).


### Paging

Result output can be displayed through your OS pager using the `--pager`/`-p`
flag.

If you're using less, add `R` to your `LESS` environment variable so colors and
styling can be displayed correctly.


### GitHub Authentication

Rate limit may be hit if starcli sends many repeated requests to GitHub within a
short perod of time.

To avoid this, provide an authentication token using `--auth`:

```
starcli --auth 'username:token'
```

[Read more about authentication tokens on GitHub
Docs](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token")


## Issues, feature request, and feedback

* Issues, bug reports, or feature request: Don't hesitate to open an issue in
  this repo
* Feedback: any general feedback or questions about using StarCLI you can leave
  a comment on the [Product Hunt
  page](https://www.producthunt.com/posts/starcli)


## Development    [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

For contributing guidelines and how to set up your development environment,
please read
[`CONTRIBUTING.md`](https://github.com/hedyhli/starcli/blob/main/CONTRIBUTING.md).
Remember that all contributions to this project should follow its [CODE OF
CONDUCT](https://github.com/hedyhli/starcli/blob/main/CODE_OF_CONDUCT.md).


## Uses

* CommandLine Argument parser: [Click](https://github.com/pallets/click)
* Colored and table console print: [`rich`](https://github.com/willmcgugan/rich)
  (with click and colorama)
* HTTP library to send requests: [`requests`](https://github.com/psf/requests)



## Contributors ✨

Thanks goes to all of these wonderful people ([emoji
key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Shagilton"><img src="https://avatars0.githubusercontent.com/u/21122143?v=4?s=100" width="100px;" alt="Shagilton"/><br /><sub><b>Shagilton</b></sub></a><br /><a href="https://github.com/hedyhli/starcli/commits?author=Shagilton" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/hexbee"><img src="https://avatars2.githubusercontent.com/u/26668583?v=4?s=100" width="100px;" alt="hexbee"/><br /><sub><b>hexbee</b></sub></a><br /><a href="https://github.com/hedyhli/starcli/issues?q=author%3Ahexbee" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/swellander"><img src="https://avatars0.githubusercontent.com/u/22231097?v=4?s=100" width="100px;" alt="Sam Wellander"/><br /><sub><b>Sam Wellander</b></sub></a><br /><a href="https://github.com/hedyhli/starcli/commits?author=swellander" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.shivamsinha.xyz/"><img src="https://avatars0.githubusercontent.com/u/32016929?v=4?s=100" width="100px;" alt="Shivam Sinha"/><br /><sub><b>Shivam Sinha</b></sub></a><br /><a href="https://github.com/hedyhli/starcli/commits?author=shivam212" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.willmcgugan.com"><img src="https://avatars3.githubusercontent.com/u/554369?v=4?s=100" width="100px;" alt="Will McGugan"/><br /><sub><b>Will McGugan</b></sub></a><br /><a href="https://github.com/hedyhli/starcli/commits?author=willmcgugan" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ashikjm"><img src="https://avatars1.githubusercontent.com/u/12744524?v=4?s=100" width="100px;" alt="Ashik J M"/><br /><sub><b>Ashik J M</b></sub></a><br /><a href="https://github.com/hedyhli/starcli/commits?author=ashikjm" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ylchao"><img src="https://avatars0.githubusercontent.com/u/15059429?v=4?s=100" width="100px;" alt="Yu-Lin Chao"/><br /><sub><b>Yu-Lin Chao</b></sub></a><br /><a href="https://github.com/hedyhli/starcli/commits?author=ylchao" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Saif807380"><img src="https://avatars2.githubusercontent.com/u/50794619?v=4?s=100" width="100px;" alt="Saif Kazi"/><br /><sub><b>Saif Kazi</b></sub></a><br /><a href="https://github.com/hedyhli/starcli/commits?author=Saif807380" title="Code">💻</a> <a href="https://github.com/hedyhli/starcli/commits?author=Saif807380" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://arcanedomain.duckdns.org"><img src="https://avatars3.githubusercontent.com/u/16456078?v=4?s=100" width="100px;" alt="arcanearronax"/><br /><sub><b>arcanearronax</b></sub></a><br /><a href="https://github.com/hedyhli/starcli/commits?author=arcanearronax" title="Tests">⚠️</a> <a href="https://github.com/hedyhli/starcli/commits?author=arcanearronax" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jSadoski"><img src="https://avatars1.githubusercontent.com/u/1865629?v=4?s=100" width="100px;" alt="jSadoski"/><br /><sub><b>jSadoski</b></sub></a><br /><a href="https://github.com/hedyhli/starcli/commits?author=jSadoski" title="Documentation">📖</a> <a href="https://github.com/hedyhli/starcli/commits?author=jSadoski" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.odmishien.fun"><img src="https://avatars3.githubusercontent.com/u/25533384?v=4?s=100" width="100px;" alt="odmishien(Tetsuya MISHIMA)"/><br /><sub><b>odmishien(Tetsuya MISHIMA)</b></sub></a><br /><a href="https://github.com/hedyhli/starcli/commits?author=odmishien" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://linkedin.com/in/ineelshah"><img src="https://avatars1.githubusercontent.com/u/40118578?v=4?s=100" width="100px;" alt="Neel Shah"/><br /><sub><b>Neel Shah</b></sub></a><br /><a href="https://github.com/hedyhli/starcli/commits?author=ineelshah" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/0xflotus"><img src="https://avatars3.githubusercontent.com/u/26602940?v=4?s=100" width="100px;" alt="0xflotus"/><br /><sub><b>0xflotus</b></sub></a><br /><a href="https://github.com/hedyhli/starcli/commits?author=0xflotus" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/AkashD-Developer"><img src="https://avatars.githubusercontent.com/u/44431401?v=4?s=100" width="100px;" alt="Akash Dhanwani"/><br /><sub><b>Akash Dhanwani</b></sub></a><br /><a href="https://github.com/hedyhli/starcli/commits?author=AkashD-Developer" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="http://cqls.oregonstate.edu"><img src="https://avatars.githubusercontent.com/u/16343359?v=4?s=100" width="100px;" alt="Ed Davis"/><br /><sub><b>Ed Davis</b></sub></a><br /><a href="https://github.com/hedyhli/starcli/commits?author=davised" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://jeetizee.com"><img src="https://avatars.githubusercontent.com/u/33030965?v=4?s=100" width="100px;" alt="Jeff Chiang"/><br /><sub><b>Jeff Chiang</b></sub></a><br /><a href="https://github.com/hedyhli/starcli/commits?author=tizee" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://dmitrykankalovich.com/"><img src="https://avatars.githubusercontent.com/u/6346981?v=4?s=100" width="100px;" alt="Dmitry Kankalovich"/><br /><sub><b>Dmitry Kankalovich</b></sub></a><br /><a href="https://github.com/hedyhli/starcli/commits?author=dzmitry-kankalovich" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the
[all-contributors](https://github.com/all-contributors/all-contributors)
specification. Contributions of any kind welcome!


## Credits

This project was forked from [`githunt`
(python)](https://github.com/SriNandan33/githunt) and its initial intention was
to rewrite that project to use Rich instead of colorama + tabulate, but now it
has so much more features than before, thanks to everyone's contributions 🙌
