""" starcli.list_output """

# Standard library imports
import textwrap

# Third party imports
from rich.console import Console
from rich.table import Table

from .terminal_size import terminal_size


def list_layout(repos):
    """ Displays repositories in list layout using rich """

    console = Console()  # initialise rich
    separator = "+==============================================================+"
    term_width, _ = terminal_size()
    side_width = int((term_width - len(separator)) / 2)

    console.print(separator, justify="center", end="\n\n")
    for repo in repos:
        console.print(
            " " * side_width,
            "[link=" + repo["html_url"] + "]" + repo["full_name"] + "[/link]",
            style="yellow",
            end="\t",
        )
        console.print(
            f"{repo['stargazers_count']}:star:, ", style="bold magenta", end=" "
        )
        console.print(
            f"{repo['forks_count']}:fork_and_knife:, ", style="bold yellow", end=" "
        )
        console.print(f"{repo['watchers_count']}:eyes:", style="bold cyan", end="\n\n")
        console.print(" " * side_width, repo["language"], style="bold cyan", end="\n\n")
        console.print(
            " " * side_width,
            ("\n" + " " * side_width).join(
                textwrap.wrap(f"{repo['description']}", len(separator))
            ),
            style="green",
            end="\n\n",
        )
        console.print(separator, justify="center", end="\n\n")
