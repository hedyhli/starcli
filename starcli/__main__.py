""" starcli.__main__ """

# Standard library imports
from datetime import datetime, timedelta

# Third party imports
import click
import requests
from rich.console import Console

# Internal application imports
from .list_layout import list_layout
from .table_layout import table_layout
from .search import search

API_URL = "https://api.github.com/search/repositories"
console = Console()


@click.command()
@click.option("--language", "-l", default="", help="language filter (eg: python)")
@click.option(
    "--date",
    "-d",
    default="",
    help="date in the ISO8601 format which is YYYY-MM-DD (year-month-day)",
)
@click.option(
    "--layout",
    "-L",
    default="list",
    help="output format, it can be either table or list",
)
@click.option(
    "--stars",
    "-s",
    default=">=50",
    help="Specify the range of stars needed. Default: >=50",
)
def cli(language, date, layout, stars):
    repos = search(language, date, stars)
    if layout == "table":
        table_layout(repos)
        return
    list_layout(repos)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()
