# Contributing


**Working on your first Pull Request?** You can learn how from this *free* series [How to Contribute to an Open Source Project on GitHub](https://egghead.io/series/how-to-contribute-to-an-open-source-project-on-github)

---

Thanks for taking the time to look at `CONTRIBUTING.md`.

All contributions to this project should follow the `CODE_OF_CONDUCT.md`.

### Reporting issues and providing feedback

If you found any issues or bugs, be sure to open up an issue so I can check it out!

Starcli does not have a chat community as of now, so any feedback you have, you can leave a comment on [StarCLI's product hunt page](https://www.producthunt.com/posts/starcli/maker-invite?code=gMzkzM), remember to be nice. 🙂

### Opening a pull request

Once you've worked on your feature/bugfix etc, you can open a pull request using the `main` branch as the base branch. Write a clear and concise PR title, and a detailed description of why you made the change, whether it is related to any issues etc. And I will review it as soon as I can.

### Setting up development environment

This project is written in Python, requires **Python 3.6 or higher**, and uses `pip` with `setup.py`.

To set it up, just fork + clone it, create a virtual environment and install all the dependencies:

```bash
$ pip install -r requirements_dev.txt
```

The command will install all the requirements needed to run starcli, as well as dev-dependencies like `black`, `pylint`, `codespell`, etc.

Remember to use the `python3` and `pip3` command instead of `python` and `pip` if your system also has Python 2 installed.

Alternatively, if you're going to use `pipenv`, you will need to use the `--pre` flag when installing in order for `black` to work:

```bash
$ pipenv install -r requirements_dev.txt --pre
```

Check if the setup worked by running starcli from your local folder. 

```bash
$ python -m starcli --help
```

If the above command displayed the help and usage, you are good to go 👍 you can also test all
the other features like list and table output, debug, etc. 

**Running tests**
```bash
python -m pytest
```

or, for authenticated requests:

```bash
python -m pytest --auth [username]:[token]
```

Where **username** = your GitHub username and **token** = a [personal access token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token). Authenticating your request will allow you to test authentication features and use a higher rate limit with the GitHub API. *This token does not need any permissions!*

**Linting checks**

```bash
pylint *.py
```

**Formatting & code spell**
```bash
black . && codespell --skip=".git,*.json,demo-pics/,venv/"
```
