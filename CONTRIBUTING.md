# Contributing


**Working on your first Pull Request?** You can learn how from this free
series [How to Contribute to an Open Source Project on
GitHub](https://egghead.io/series/how-to-contribute-to-an-open-source-project-on-github)


Thanks for taking the time to look at `CONTRIBUTING.md`.

All contributions to this project should follow the `CODE_OF_CONDUCT.md`.

### Reporting issues and providing feedback

If you found any issues or bugs, be sure to open up an issue so someone can
check it out!


### Opening a pull request

Once you've worked on your feature/bugfix etc, you can open a pull request using
the `main` branch as the base branch. Write a clear and concise PR title, and a
detailed description of why you made the change, whether it is related to any
issues etc. And I will review it as soon as I can.

### Setting up development environment

This project is written in Python, requires **Python 3.6 or higher**, and uses
`pip` with `setup.py`.

To set it up, just [fork](https://github.com/hedyhli/starcli/fork) + clone it,
create a [virtual environment](https://virtualenv.pypa.io/en/latest/) and
install all the dependencies:

```bash
$ pip install -r requirements_dev.txt
```

The command will install all the requirements needed to run starcli, as well as
dev-dependencies like [black](https://github.com/psf/black),
[pylint](https://www.pylint.org/),
[codespell](https://github.com/codespell-project/codespell) and
[pytest](https://pytest.org).

> Remember to use the `python3` and `pip3` commands instead of `python` and
> `pip` if your system also has Python 2 installed.

Alternatively, if you're going to use `pipenv`, you will need to use the `--pre`
flag when installing in order for `black` to work:

```bash
$ pipenv install -r requirements_dev.txt --pre
```

Check if the setup worked by running starcli from your local folder.

```bash
$ python -m starcli --help
```

If the above command displayed the help and usage, you are good to go 👍 you can
also test all the other features like list and table output, debug, etc.

**Running tests**
```bash
python -m pytest
```

or, for authenticated requests:

```bash
python -m pytest --auth username:token
```

Where **username** is your GitHub username and **token** is a
[personal access token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token).
Authenticating your request will allow you to test authentication features and
use a higher rate limit with the GitHub API. *This token does not need any permissions!*

Note that if the the value passed to `--auth` is invalid, some tests will fail.
So check with `starcli --auth` if some tests are mysteriously failing when using
`--auth`.

**Linting checks**

```bash
pylint *.py
```

**Formatting & code spell**
```bash
black . && codespell --skip=".git,*.json,demo-pics/,venv/"
```
