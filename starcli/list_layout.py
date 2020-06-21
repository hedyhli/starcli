""" starcli.list_output """

# Standard library imports
import textwrap

# Third party imports
from rich.console import Console
from rich.table import Table


def list_layout(repos):
    """ Displays repositories in list layout using rich """

    console = Console()  # initialise rich
    separator = "+==================================================================+"
    console.print(separator, end="\n\n")
    for repo in repos:
        console.print(
            "[link=" + repo["html_url"] + "]" + repo["full_name"] + "[/link]",
            style="yellow",
        )
        console.print(
            "\n  ".join(textwrap.wrap(f"{repo['description']}", len(separator))),
            style="green",
            end="\n\n",
        )
        console.print(repo["language"], style="bold cyan", end="\t")
        console.print(
            f"{repo['stargazers_count']}:star:, ", style="bold magenta", end="\t"
        )
        console.print(
            f"{repo['forks_count']}:fork_and_knife:, ", style="bold yellow", end="\t"
        )
        console.print(f"{repo['watchers_count']}:eyes:", style="bold cyan", end="\n\n")
        console.print(separator, end="\n\n")
