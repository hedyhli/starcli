""" Formats repositories in console """

# Standard library imports
import textwrap

# Third party imports
from colorama import init, Fore, Style
from tabulate import tabulate
from rich.console import Console

console = Console()

# def make_hyperlink(text, target):
    # """ Makes hyperlink out of text and target and retuns it
        # https://stackoverflow.com/questions/44078888/clickable-html-links-in-python-3-6-shell
    # """
    # return f"\u001b]8;;{target}\u001b\\{text}\u001b]8;;\u001b\\"


def colored_output(repos):
    """ Displays repositories using rich """

    init()  # initialize coloroma
    seperator = "+==================================================================+"
    console.print("[white]", seperator, end="\n\n")
    for repo in repos:
        console.print(
            "[yellow]",
            repo['name'],
            repo['html_url']
        )
        console.print(
            "[yellow]",
            "\n  ".join(textwrap.wrap(f"{repo['description']}", len(seperator))),
            end="\n\n",
        )
        console.print("[bold cyan]", repo['language'], end="\t")
        console.print(
            "[bold magenta]"
            f"repo['stargazers_count']",
            " Stars",
            end="\t",
        )
        console.print(f"[bold yellow]{repo['forks_count']} Forks", end="\t")
        console.print(
            "[blue]",
            str(repo['watchers_count']),
            " Watchers",
            end="\n\n",
        )
        console.print("[white]", seperator, end="\n\n")


def tabular_output(repos):
    """ Displays repositories as tables using tabulate """
    table_headers = ["URL", "Language", "Stars", "Forks", "Watches"]
    repositories = [
        [
            repo["html_url"],
            repo["language"],
            repo["stargazers_count"],
            repo["forks_count"],
            repo["watchers_count"],
        ]
        for repo in repos
    ]
    print(tabulate(repositories, headers=table_headers, tablefmt="fancy_grid"))


# def beautify(repos, fmt):
    # """ Beautfies the output based on display format given """
    # if fmt == "colored":
        # colored_output(repos)
    # elif fmt == "table":
        # tabular_output(repos)
    # else:
        # print("Can't output anything. Invalid display format!")
