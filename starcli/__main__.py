""" starcli.__main__ """

from argparse import Namespace

import click

from .layouts import list_layout, table_layout
from .search import search

# from .parser import args


@click.command()
@click.option("--lang", "-l", type=str, default="", help="Language filter eg: python")
@click.option(
    "--date",
    "-d",
    default="",
    help="Specify repo creation date in ISO8601 format YYYY-MM-DD",
)
@click.option(
    "--layout",
    "-L",
    type=click.Choice(["list", "table"], case_sensitive=False),
    help="The output format (list or table), default is list",
)
@click.option(
    "--stars",
    "-s",
    type=str,
    default=">=50",
    help="Range of stars required, default is '>=50'",
)
@click.option(
    "--limit-results",
    "-r",
    type=int,
    default=7,
    help="Limit the number of results shown. Default: 7",
)
@click.option(
    "--order",
    "-o",
    type=click.Choice(["desc", "asc"], case_sensitive=False),
    default="desc",
    help="Specify the order of repos by stars that is shown, 'desc' or 'asc', default: desc",
)
@click.option("--debug", is_flag=True, default=False, help="Turn on debugging mode")
def cli(lang, date, layout, stars, limit_results, order, debug):
    """ Browse trending repos on GitHub by stars """

    tmp_repos = search(lang, date, stars, debug, order)
    if not tmp_repos:  # if search() returned None
        return

    repos = []
    for i in range(limit_results):
        repos.append(tmp_repos[i])

    if layout == "table":
        table_layout(repos)
        return
    list_layout(repos)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()
