"""starcli.search

The search module responsible for handling requests and querying GitHub
"""

# Standard library imports
from datetime import datetime, timedelta
from time import sleep
import logging
from random import randint
import re
import http.client
import typing as t

# Third party imports
import requests
from click import secho
import gtrending
from rich.logging import RichHandler

API_URL = "https://api.github.com/search/repositories"

# "X stars today" / "X stars this week"
# today, this week, this month must be first item in the tuple for use in date_range_str()
DATE_RANGE_MAP = {
    "daily": ("today", "day"),
    "weekly": ("this week", "week"),
    "monthly": ("this month", "month"),
}

STATUS_ACTIONS = {
    "retry": "Failed to retrieve data. Retrying in ",
    "invalid": "The server was unable to process the request.",
    "unauthorized": "The server did not accept the credentials.\n" \
        "See: https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token\n" #
        "Maybe you did not give enough scopes?",
    "not_found": "The server indicated no data was found.",
    "unsupported": "The request is not supported.",
    "unknown": "An unknown error occurred.",
    "valid": "The request returned successfully, but an unknown exception occurred.",
}

FORMAT = "%(message)s"

httpclient_logger = logging.getLogger("http.client")


def httpclient_logging_debug(level=logging.DEBUG):
    def httpclient_log(*args):
        httpclient_logger.log(level, " ".join(args))

    http.client.print = httpclient_log
    http.client.HTTPConnection.debuglevel = 1


def debug_requests_on():
    """Turn on the logging for requests"""
    logging.basicConfig(
        level=logging.DEBUG,
        format=FORMAT,
        datefmt="[%Y-%m-%d]",
        handlers=[RichHandler()],
    )
    logger = logging.getLogger(__name__)

    from http.client import HTTPConnection

    httpclient_logging_debug()

    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


def debug_logger(debug: bool, *args, **kwargs):
    """Log a message if debug mode is on"""
    if debug:
        debug_requests_on()
        logger = logging.getLogger(__name__)
        logger.debug(*args, **kwargs)


def convert_datetime(date: str, date_format: str = "%Y-%m-%d"):
    """Safely convert a date string to datetime"""
    try:
        # try to turn the string into a date-time object
        tmp_date = datetime.strptime(date, date_format)
    except ValueError:  # ValueError will be thrown if format is invalid
        secho(
            f"Invalid date format: {date}. Must be yyyy-mm-dd",
            fg="bright_red",
        )
        return None
    return tmp_date


def get_date(date):
    """Find the date info in a string"""
    prefix = ""
    if any(i in date[0] for i in [">", "=", "<"]):
        if "=" in date[1]:
            prefix = date[:2]
            date = date.strip(prefix)
        else:
            prefix = date[0]
            date = date.strip(prefix)
    tmp_date = convert_datetime(date)
    if not tmp_date:
        return None
    return prefix + tmp_date.strftime("%Y-%m-%d")


def get_valid_request(
    url: str, auth: t.Optional[str] = ""
) -> t.Optional[requests.Response]:
    """GET an url with auth and handle a connection error"""
    while True:
        try:
            session = requests.Session()
            if auth:
                session.auth = (auth.split(":")[0], auth.split(":")[1])
            request = session.get(url)
        except requests.exceptions.ConnectionError:
            secho("Internet connection error...", fg="bright_red")
            return

        if not request.status_code in (200, 202):
            handling_code = search_error(request.status_code)
            if handling_code == "retry":
                for i in range(15, 0, -1):
                    secho(
                        f"{STATUS_ACTIONS[handling_code]} {i} seconds...",
                        fg="bright_yellow",
                    )  # Print and update a timer

                    sleep(1)
            elif handling_code in STATUS_ACTIONS:
                secho(STATUS_ACTIONS[handling_code], fg="bright_yellow")
                return
            else:
                secho("An invalid handling code was returned.", fg="bright_red")
                return
        else:
            break

    return request


def search_error(status_code: t.Union[int, str]):
    """Get a directive on how to handle a given HTTP status code"""
    int_status_code = int(status_code)  # Make sure the status code is an integer

    http_code_handling = {
        "200": "valid",
        "202": "valid",
        "204": "valid",
        "400": "invalid",
        "401": "unauthorized",
        "403": "retry",
        "404": "not_found",
        "405": "invalid",
        "422": "not_found",
        "500": "invalid",
        "501": "invalid",
    }

    try:
        return http_code_handling[str(int_status_code)]
    except KeyError:
        return "unsupported"


def convert_date_range(param: str) -> t.Optional[str]:
    """Convert the date range parameter into 'since' parameter for GitHub Trending"""
    if not param:
        return None
    param = param.lower().replace(" ", "-")
    for key, aliases in DATE_RANGE_MAP.items():
        if param == key or param in aliases:
            return key
    raise ValueError(f"Invalid date range parameter: {param}")


def date_range_str(period_stars: int, since: int) -> str:
    """Generate a readable string to display the current date range stars increase

    Parameters:
        since (int): The argument used for GitHub Trending search.

    Returns:
        str: The formatted string for output.
    """
    date_range = DATE_RANGE_MAP.get(since, (None,))[0]
    return f"+{period_stars} stars {date_range}"


def search(
    languages=[""],
    created=None,
    pushed=None,
    stars=">=100",
    topics=[],
    user=None,
    debug=False,
    order="desc",
    auth="",
):
    """Return repositories searched from GitHub API"""
    date_format = "%Y-%m-%d"  # date format in iso format
    debug_logger(debug, f"Search: created param: {created}")
    debug_logger(debug, f"Search: order param: {order}")

    day_range = 0 - randint(100, 400)  # random negative from 100 to 400

    if not created:  # if created not provided
        # creation date: the time now minus a random number of days
        # 100 to 400 days - which was stored in day_range
        created_str = ">=" + (datetime.utcnow() + timedelta(days=day_range)).strftime(
            date_format
        )
    else:  # if created is provided
        created_str = get_date(created)
        if not created_str:
            return None

    if not pushed:  # if pushed not provided
        # pushed date: start, is the time now minus a random number of days
        # 100 to 400 days - which was stored in day_range
        pushed_str = ">=" + (datetime.utcnow() + timedelta(days=day_range)).strftime(
            date_format
        )
    else:  # if pushed is provided
        pushed_str = get_date(pushed)
        if not pushed_str:
            return None

    query = ""
    if user:
        query = f"user:{user}+"

    query += f"stars:{stars}+created:{created_str}"  # construct query
    query += f"+pushed:{pushed_str}"  # add pushed info to query
    query += "".join(
        [f"+language:{language}" for language in languages]
    )  # add language to query
    query += "".join(["+topic:" + i for i in topics])  # add topics to query

    url = f"{API_URL}?q={query}&sort=stars&order={order}"  # use query to construct url
    debug_logger(debug, f"Search: url: {url}")
    if auth:
        debug_logger(debug, "Auth: on")
    else:
        debug_logger(debug, "Auth: off")

    request = get_valid_request(url, auth)
    if request is None:
        return request

    return request.json()["items"]


def search_github_trending(
    languages=[""],
    spoken_language=None,
    order="desc",
    stars=">=10",
    date_range=None,
    debug=False,
) -> t.List[dict]:
    """Returns trending repositories from github trending page"""
    gtrending_repo_list = []
    since = convert_date_range(date_range)

    debug_logger(debug, f"gtrending: since: {since}")

    for language in languages:
        if date_range:
            debug_logger(
                debug,
                f"gtrending: fetching repos: language={language}, spoken_language={spoken_language}, since={since}",
            )
            gtrending_repo_list += gtrending.fetch_repos(
                language, spoken_language, since
            )
        else:
            debug_logger(
                debug,
                f"gtrending: fetching repos: language={language}, spoken_language={spoken_language}",
            )
            gtrending_repo_list += gtrending.fetch_repos(language, spoken_language)

    repositories = []
    for gtrending_repo in gtrending_repo_list:
        repo_dict = convert_repo_dict(gtrending_repo)
        repo_dict["date_range"] = (
            date_range_str(repo_dict["date_range"], since) if date_range else None
        )
        # filter by number of stars
        num = [int(s) for s in re.findall(r"\d+", stars)][0]
        if (
            ("<" in stars and repo_dict["stargazers_count"] < num)
            or ("<=" in stars and repo_dict["stargazers_count"] <= num)
            or (">" in stars and repo_dict["stargazers_count"] > num)
            or (">=" in stars and repo_dict["stargazers_count"] >= num)
        ):
            repositories.append(repo_dict)

    if order == "asc":
        return sorted(repositories, key=lambda repo: repo["stargazers_count"])
    return sorted(repositories, key=lambda repo: repo["stargazers_count"], reverse=True)


def convert_repo_dict(gtrending_repo: dict) -> dict:
    """Normalize dictionary keys returned by gtrending"""
    repo_dict = {}
    repo_dict["full_name"] = gtrending_repo.get("fullname")
    repo_dict["name"] = gtrending_repo.get("name")
    repo_dict["html_url"] = gtrending_repo.get("url")
    repo_dict["stargazers_count"] = gtrending_repo.get("stars", -1)
    repo_dict["forks"] = gtrending_repo.get("forks", -1)
    repo_dict["language"] = gtrending_repo.get("language")
    # gtrending_repo has key `description` and value is empty string if it's empty
    repo_dict["description"] = (
        gtrending_repo.get("description")
        if gtrending_repo.get("description") != ""
        else None
    )
    repo_dict["date_range"] = gtrending_repo.get("currentPeriodStars")
    return repo_dict
