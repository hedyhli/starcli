""" starcli.layouts """

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
            f"[link={repo['html_url']}]{repo['full_name']}[/link]",
            style="yellow",
            end="  ",
        )

        stats = (
            str(repo["stargazers_count"])
            + ":star:, "
            + str(repo["forks_count"])
            + ":fork_and_knife:, "
            + str(repo["watchers_count"])
            + ":eyes:"
        )

        if len(repo["full_name"] + stats) > len(separator + "   "):
            print()
            console.print(
                " " * ((side_width) + (len(separator) - len(stats))), stats, end="\n\n"
            )
        else:
            console.print(stats, end="\n\n")

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


def table_layout(repos):
    """ Displays repositories in a table format using rich """
    table = Table()

    table.add_column("Name", style="bold cyan", no_wrap=True, width=45)
    table.add_column("Language", style="green", no_wrap=True, width=23)
    table.add_column("Description", style="blue", no_wrap=False, width=160)
    table.add_column("Stats", style="magenta", no_wrap=True, width=45)

    for repo in repos:
        stats = (
            str(repo["stargazers_count"])
            + ":star:, "
            + str(repo["forks_count"])
            + ":fork_and_knife:, "
            + str(repo["watchers_count"])
            + ":eyes:"
        )

        if not repo["language"]:  # if language is not provided
            repo["language"] = "None"  # make it a string
        if not repo["description"]:
            repo["description"]: "None"

        table.add_row(
            repo["name"] + "\n\n",
            repo["language"] + "\n\n",  # so that it can work here
            repo["description"],
            stats,
        )

    console = Console()
    console.print(table)
