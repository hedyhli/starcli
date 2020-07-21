""" starcli.__main__ """

import click

from .layouts import list_layout, table_layout, grid_layout, shorten_count
from .search import search, debug_requests_on, search_by_spoken_language


@click.command()
@click.option("--lang", "-l", type=str, default="", help="Language filter eg: python")
@click.option(
    "--spoken-language",
    "-S",
    type=str,
    default="",
    help="Spoken Language filter eg: en for English, zh for Chinese, etc",
)
@click.option(
    "--date-created",
    "-d",
    default="",
    help="Specify repo creation date in ISO8601 format YYYY-MM-DD",
)
@click.option(
    "--topics",
    "-t",
    default="",
    multiple=True,
    help="Search by topic. Can be specified multiple times. Multiple topics will be conjugated using &",
)
@click.option(
    "--last-updated",
    "-u",
    default="",
    help="Filter repos based on time of last update in ISO8601 format YYYY-MM-DD",
)
@click.option(
    "--layout",
    "-L",
    type=click.Choice(["list", "table", "grid"], case_sensitive=False),
    help="The output format (list, table, or grid), default is list",
)
@click.option(
    "--stars",
    "-s",
    type=str,
    default=">=100",
    help="Range of stars required, default is '>=100'",
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
@click.option(
    "--long-stats", is_flag=True, help="Print the actual stats[1300 instead of 1.3k]",
)
@click.option("--debug", is_flag=True, default=False, help="Turn on debugging mode")
def cli(
    lang,
    spoken_language,
    date_created,
    topics,
    last_updated,
    layout,
    stars,
    limit_results,
    order,
    long_stats,
    debug,
):
    """ Find trending repos on GitHub """
    if debug:
        import logging

        debug_requests_on()
    if not spoken_language:  # if filtering by spoken language not required
        tmp_repos = search(
            lang, date_created, last_updated, stars, topics, debug, order
        )
    else:
        tmp_repos = search_by_spoken_language(lang, spoken_language, order, stars)
    if not tmp_repos:  # if search() returned None
        return
    repos = tmp_repos[0:limit_results]

    if not long_stats:
        for repo in repos:
            repo["stargazers_count"] = shorten_count(repo["stargazers_count"])
            repo["forks_count"] = shorten_count(repo["forks_count"])
            if repo["watchers_count"]:
                repo["watchers_count"] = shorten_count(repo["watchers_count"])
    if layout == "table":
        table_layout(repos)
        return

    if layout == "grid":
        grid_layout(repos)
        return

    list_layout(repos)  # if layout isn't a grid or table, then use list.


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()
