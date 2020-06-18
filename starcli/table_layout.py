""" starcli.table_layout """

from rich.table import Table
from rich.console import Console

def table_layout(repos):
    table = Table()

    table.add_column("Name", style="bold cyan", no_wrap=True, width=47)
    table.add_column("Language", style="green", no_wrap=True, width=20)
    table.add_column("Description", style="blue", no_wrap=False, width=150)
    table.add_column("Stats", style="magenta", no_wrap=True, width=75)

    for repo in repos:
        stats = (
            str(repo["stargazers_count"])
            + " Stars, "
            + str(repo["forks_count"])
            + " Forks, "
            + str(repo["watchers_count"])
            + " Watchers"
        )

        table.add_row(
            str(repo["name"]) + "\n",
            str(repo["language"] + "\n"),
            str(repo["description"]),
            stats,
        )

    console = Console()
    console.print(table)
