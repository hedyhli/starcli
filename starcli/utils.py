""" starcli utils """

# Standard library imports
import textwrap

# Third party imports
from rich.console import Console
from rich.table import Table


def colored_output(repos):
    """ Displays repositories using rich """

    console = Console()  # initialise rich
    seperator = "+==================================================================+"
    console.print(seperator, end="\n\n")
    for repo in repos:
        console.print(
            "[link=" + repo["html_url"] + "]" + repo["full_name"] + "[/link]",
            style="yellow",
        )
        console.print(
            "\n  ".join(textwrap.wrap(f"{repo['description']}", len(seperator))),
            style="green",
            end="\n\n",
        )
        console.print(repo["language"], style="bold cyan", end="\t")
        console.print(
                f"{repo['stargazers_count']} :star:, ", style="bold magenta", end="\t",
        )
        console.print(f"{repo['forks_count']} Forks, ", style="bold yellow", end="\t")
        console.print(
            f"{repo['watchers_count']} Watchers", style="bold cyan", end="\n\n"
        )
        console.print(seperator, end="\n\n")


def table_output(repos):
    table = Table()

    table.add_column("Name", style="bold cyan", no_wrap=True, width=47)
    table.add_column("Language", style="green", no_wrap=True, width=20)
    table.add_column("Description", style="blue", no_wrap=False, width=150)
    table.add_column("Stats", style="magenta", no_wrap=True, width=75)

    for repo in repos:
        stats = str(repo['stargazers_count']) + " Stars, " + \
            str(repo['forks_count']) + " Forks, " + \
            str(repo['watchers_count']) + " Watchers"

        table.add_row(
                str(repo["name"]) + "\n",
                str(repo["language"] + "\n"),
                str(repo["description"]),
                stats
            )

    console = Console()
    console.print(table)

