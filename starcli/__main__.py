""" starcli.__main__ """

from time import sleep

import click
from requests.exceptions import HTTPError
import re

from .layouts import list_layout, table_layout, grid_layout, shorten_count
from .search import (
    search,
    debug_requests_on,
    search_github_trending,
    search_error,
    status_actions,
)


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
    "--created",
    "-c",
    default="",
    help="Specify repo creation date in YYYY-MM-DD, prefixing with >, <= etc is allowed",
)
@click.option(
    "--topic",
    "-t",
    default="",
    multiple=True,
    help="Search by topic, can be specified multiple times",
)
@click.option(
    "--pushed",
    "-p",
    default="",
    help="Specify date of last push in YYYY-MM-DD, >=< allowed",
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
    help="Amount of stars required, default is '>=100'. Can use 123, <10, etc.",
)
@click.option(
    "--limit-results",
    "-r",
    type=int,
    default=7,
    help="Limit the number of results. Default: 7",
)
@click.option(
    "--order",
    "-o",
    type=click.Choice(["desc", "asc"], case_sensitive=False),
    default="desc",
    help="Order of repos by stars shown, 'desc' or 'asc', default: desc",
)
@click.option(
    "--long-stats",
    is_flag=True,
    help="Print the actual stats number (1300 instead of 1.3k)",
)
@click.option(
    "--date-range",
    "-d",
    type=click.Choice(["today", "this-week", "this-month"], case_sensitive=False),
    help="View stars received within time range, choose from: today, this-week, this-month",
)
@click.option(
    "--user",
    "-u",
    type=str,
    default="",
    help="Search for trending repositories by username",
)
@click.option(
    "--auth",
    type=str,
    default="",
    help="GitHub personal access token in the format 'username:password'.",
)
@click.option("--debug", is_flag=True, default=False, help="Turn on debugging mode")
def cli(
    lang,
    spoken_language,
    created,
    topic,
    pushed,
    layout,
    stars,
    limit_results,
    order,
    long_stats,
    date_range,
    user,
    debug=False,
    auth="",
):
    """ Find trending repos on GitHub """
    if debug:
        import logging

        debug_requests_on()

    if auth and not re.search(".:.", auth):  # check authentication format
        click.secho(
            f"Invalid authentication format: {auth} must be 'username:token'",
            fg="bright_red",
        )
        click.secho(
            "Use --help or see: https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token",
            fg="bright_red",
        )
        auth = None

    while True:
        try:
            if (
                not spoken_language and not date_range
            ):  # if filtering by spoken language and date range not required
                tmp_repos = search(
                    lang, created, pushed, stars, topic, user, debug, order, auth
                )
            else:
                tmp_repos = search_github_trending(
                    lang, spoken_language, order, stars, date_range
                )
            break  # Need this here to break out of the loop if the request is successful
        except HTTPError as e:  # If a request is unsuccessful
            status_code = str(e).split(" ")[3]
            handling_code = search_error(status_code)
            if handling_code == "retry":
                for i in range(15, 0, -1):
                    click.secho(
                        f"{status_actions[handling_code]} {i} seconds...",
                        fg="bright_yellow",
                    )  # Print and update a timer
                    sleep(1)
            elif handling_code in status_actions:
                click.secho(status_actions[handling_code], fg="bright_yellow")
                return
            else:
                click.secho("An invalid handling code was returned.", fg="bright_red")
                return

    if not tmp_repos:  # if search() returned None
        return
    repos = tmp_repos[0:limit_results]

    if not long_stats:  # shorten the stat counts when not --long-stats
        for repo in repos:
            repo["stargazers_count"] = shorten_count(repo["stargazers_count"])
            repo["forks_count"] = shorten_count(repo["forks_count"])
            repo["watchers_count"] = shorten_count(repo["watchers_count"])
            if "date_range" in repo.keys() and repo["date_range"]:
                num_stars = repo["date_range"].split()[0]
                repo["date_range"] = repo["date_range"].replace(
                    num_stars, str(shorten_count(int(num_stars.replace(",", ""))))
                )

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
