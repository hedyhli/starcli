"""starcli.__main__

The main CLI module of starcli.
"""

import re
import json
import os
from datetime import datetime, timedelta

import click
from xdg import XDG_CACHE_HOME

from .layouts import print_results, shorten_count
from .search import (
    search,
    debug_requests_on,
    search_github_trending,
    # search_error,
    # status_actions,
)


# could be made into config option in the future
CACHE_DIR = XDG_CACHE_HOME / "starcli"
CACHED_RESULT_PATH = CACHE_DIR / "results.json"
CACHED_RESULT_PATH_LEGACY = XDG_CACHE_HOME / "starcli.json"
CACHE_EXPIRATION = 1  # Minutes


@click.command()
@click.option(
    "--lang",
    "-l",
    multiple=True,
    type=str,
    default=[""],
    help="Language filter eg: python. (can be used multiple times)",
)
@click.option(
    "--spoken-language",
    "-S",
    type=str,
    default="",
    help="Spoken Language filter eg: en for English, zh for Chinese",
)
@click.option(
    "--created",
    "-c",
    default="",
    help="Specify repo creation date in YYYY-MM-DD, use >date, <=date etc to be more specific.",
)
@click.option(
    "--topic",
    "-t",
    default=[],
    multiple=True,
    help="Date of last push in YYYY-MM-DD (>, <, >=, <= specifiers supported)",
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
    help="Number of stars, default is '>=100'. eg: '>0', '123', '<50000",
)
@click.option(
    "--num-results",
    "-n",
    type=int,
    default=7,
    help="The number of items in the results. Default: 7",
)
@click.option(
    "--order",
    "-o",
    type=click.Choice(["desc", "asc"], case_sensitive=False),
    default="desc",
    help="Order of repos by stars, 'desc' or 'asc', default: desc",
)
@click.option(
    "--long-stats",
    is_flag=True,
    help="Print the actual stats number (1300 instead of 1.3k)",
)
@click.option(
    "--date-range",
    "-d",
    type=click.Choice(["day", "week", "month"], case_sensitive=False),
    help="View stars received within time, choose from: day, week, month. Uses GitHub trending for fetching results, hence some other filter options may not work.",
)
@click.option(
    "--user",
    "-u",
    type=str,
    default="",
    help="Filter for trending repositories by username",
)
@click.option(
    "--auth",
    type=str,
    default="",
    help="Optionally use GitHub personal access token in the format 'username:password'.",
)
@click.option(
    "--pager",
    "-P",
    is_flag=True,
    default=False,
    help="Use $PAGER to page output. (put -r in $LESS to enable ANSI styles)",
)
@click.option(  # Used for debugging CLI input, prevent hitting GitHub API when we don't need it
    "--nop",
    is_flag=True,
    default=False,
    hidden=True,
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
    num_results,
    order,
    long_stats,
    date_range,
    user,
    debug=False,
    auth="",
    pager=False,
    nop=False,
):
    """Find trending repos on GitHub"""
    if debug:
        import logging

        debug_requests_on()

    tmp_repos = None
    options_key = "{lang}_{spoken_language}_{created}_{topic}_{pushed}_{stars}_{order}_{date_range}_{user}".format(
        lang=lang,
        spoken_language=spoken_language,
        created=created,
        topic=topic,
        pushed=pushed,
        stars=stars,
        order=order,
        date_range=date_range,
        user=user,
    )

    if os.path.exists(CACHED_RESULT_PATH):
        with open(CACHED_RESULT_PATH, "r") as f:
            json_file = json.load(f)
            result = json_file.get(options_key)
            if result:
                t = result[-1].get("time")
                time = datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f")
                diff = datetime.now() - time
                if diff < timedelta(minutes=CACHE_EXPIRATION):
                    if debug:
                        logger = logging.getLogger(__name__)
                        logger.debug("Fetching results from cache")

                    tmp_repos = result

    if not tmp_repos:  # If cache expired or results not yet cached
        if auth and not re.search(".+:.+", auth):  # Check authentication format
            click.secho(
                f"Invalid authentication format: {auth}. Must be 'username:token'",
                fg="bright_red",
            )
            click.secho(
                "Use --help or see: "
                "https://docs.github.com/en/github/authenticating-to-github/"
                "creating-a-personal-access-token",
                fg="bright_red",
            )
            auth = None

        if nop:
            return

        if (
            not spoken_language and not date_range
        ):  # if filtering by spoken language and date range not required
            tmp_repos = search(
                lang, created, pushed, stars, topic, user, debug, order, auth
            )
        else:
            tmp_repos = search_github_trending(
                lang, spoken_language, order, stars, date_range, debug
            )

        if not tmp_repos:  # if search() returned None
            return
        else:  # Cache results
            tmp_repos.append({"time": str(datetime.now())})
            # make sure ~/.cache dir exists
            os.makedirs(CACHE_DIR, exist_ok=True)
            # Clean legacy cache file path
            try:
                os.remove(CACHED_RESULT_PATH_LEGACY)
            except FileNotFoundError:
                pass

            with open(CACHED_RESULT_PATH, "a+") as f:
                if os.path.getsize(CACHED_RESULT_PATH) == 0:  # file is empty
                    result_dict = {options_key: tmp_repos}
                    f.write(json.dumps(result_dict, indent=4))
                else:  # file is not empty
                    f.seek(0)
                    result_dict = json.load(f)
                    result_dict[options_key] = tmp_repos
                    f.truncate(0)
                    f.write(json.dumps(result_dict, indent=4))

    repos = tmp_repos[0:num_results]

    if not long_stats:  # shorten the stat counts when not using --long-stats
        for repo in repos:
            repo["stargazers_count"] = shorten_count(repo["stargazers_count"])
            repo["forks"] = shorten_count(repo["forks"])
            if "date_range" in repo.keys() and repo["date_range"]:
                num_stars = repo["date_range"].split()[0]
                repo["date_range"] = repo["date_range"].replace(
                    num_stars, str(shorten_count(int(num_stars.replace(",", ""))))
                )

    print_results(repos, page=pager, layout=layout)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()
