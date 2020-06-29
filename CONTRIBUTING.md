# Contributing


**Working on your first Pull Request?** You can learn how from this *free* series [How to Contribute to an Open Source Project on GitHub](https://egghead.io/series/how-to-contribute-to-an-open-source-project-on-github)

Thanks for taking the time to look at `CONTRIBUTING.md`, we appreciate your time. 

All contributions to this project should follow the `CODE_OF_CONDUCT.md`.

### Reporting issues and providing feedback

If you found any issues or bugs, be sure to open up an issues so I can check it out!

Starcli does not have a chat community as of now, so any feedback you have, you can leave a comment on [StarCLI's product hunt page](https://www.producthunt.com/posts/starcli/maker-invite?code=gMzkzM), remember to be nice. 🙂

### Opening a pull request

Once you've worked on your feature/bugfix etc, you can open a pull request using the `develop` branch as the base branch. Write a clear and concise PR title, and a detailed description of why you made the change, whether it is related to any issues etc. And I will review it as soon as I can.

### Setting up development environment

This project is written in Python, requires at **Python 3.6 or higher**, and uses `pip` with `setup.py`.

Before you set up your environment, you must at least have the appropriate version of Python and Pip on your PATH, with a recent version of Git on your system.

To setup your environment, first **fork** this repo

and clone it

```bash
$ git clone https://github.com/<your_username>/starcli.git
$ cd starcli
```

Then, create a virtual environment to manage the dependencies needed for starcli. Name it anything you like, but most people name it `venv` or `env`. Don't worry about accidentally pushing the folder onto GitHub, these folders are ignored by git through the `.gitignore`file. *You can use another virtual environment tool if you like, of course.*

```bash
$ python -m virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements_dev.txt
```

The `pip install` command will install all the requirements needed to run starcli, as well as dev-dependencies like `black`, `pylint`, `codespell`, etc.

Remember to use the `python3` and `pip3` command instead of `python` and `pip` if system also has Python 2 installed.

Check if the setup worked by running starcli from your local folder. 

```bash
(venv) $ python -m starcli --help
```

If the above command displayed the help and usage, you are good to go 👍

---
