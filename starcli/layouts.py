""" starcli.layouts """

# Standard library imports
import textwrap
import math
from shutil import get_terminal_size

# Third party imports
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich.columns import Columns


def shorten_count(number):
    """Shortens number"""
    if number < 1000:
        return str(number)

    number = int(number)
    new_number = math.ceil(round(number / 100.0, 1)) * 100

    if new_number % 1000 == 0:
        return str(new_number)[0] + "k"
    if new_number < 1000:
        # returns the same old integer if no changes were made
        return number
    else:
        # returns a new string if the number was shortened
        return str(new_number / 1000.0) + "k"


def list_layout(repos):
    """ Displays repositories in list layout using rich """

    console = Console()  # initialise rich
    separator = "+==============================================================+"
    term_width = get_terminal_size().columns
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
            + "⭐, "
            + str(repo["forks_count"])
            + "🍴, "
            + str(repo["watchers_count"])
            + "👀"
        )

        if len(repo["full_name"] + stats) > len(separator + " "):
            print()
            console.print(
                " " * ((side_width) + (len(separator) - len(stats))),
                stats,
                end="\n\n",
                style="blue",
            )
        else:
            console.print(stats, end="\n\n", style="blue")

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
    table.add_column("Description", style="blue", no_wrap=True, width=140)
    table.add_column("Stats", style="magenta", no_wrap=False, width=57)

    for repo in repos:
        stats = (
            str(repo["stargazers_count"])
            + "⭐, "
            + str(repo["forks_count"])
            + "🍴, "
            + str(repo["watchers_count"])
            + "👀"
        )

        if not repo["language"]:  # if language is not provided
            repo["language"] = "None"  # make it a string
        if not repo["description"]:
            repo["description"] = "None"

        table.add_row(
            repo["name"] + "\n\n",
            repo["language"] + "\n\n",  # so that it can work here
            repo["description"],
            stats,
        )

    console = Console()
    console.print(table)


def grid_layout(repos):
    """ Displays repositories in a grid format using rich """

    max_description_len = 90

    panels = []
    for repo in repos:

        stats = (
            str(repo["stargazers_count"])
            + "⭐, "
            + str(repo["forks_count"])
            + "🍴, "
            + str(repo["watchers_count"])
            + "👀"
        )

        if not repo["language"]:  # if language is not provided
            repo["language"] = "None"  # make it a string
        if not repo["description"]:
            repo["description"] = "None"

        if len(repo["description"]) > max_description_len:
            repo["description"] = (
                repo["description"][: max_description_len - 1].strip() + "…"
            )

        name = Text(repo["name"], style="bold yellow")
        language = Text(repo["language"], style="magenta")
        description = Text(repo["description"], style="green")
        stats = Text(stats, style="blue")

        repo_summary = Text.assemble(
            name, "\n", stats, "\n", language, "\n", description,
        )
        panels.append(Panel(repo_summary, expand=True))

    console = Console()
    console.print((Columns(panels, width=30, expand=True)))
