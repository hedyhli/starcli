""" starcli.table_layout """

from rich.table import Table
from rich.console import Console


def table_layout(repos):
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
