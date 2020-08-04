""" starcli.search """

# Standard library imports
from datetime import datetime, timedelta
import logging
from random import randint
import re

# Third party imports
import requests
from click import secho
import colorama
from bs4 import BeautifulSoup

API_URL = "https://api.github.com/search/repositories"

date_range_map = {"today": "daily", "this-week": "weekly", "this-month": "monthly"}

status_actions = {
    "retry": "Failed to retrieve data. Retrying in ",
    "invalid": "The server was unable to process the request.",
    "unauthorized": "The server did not accept the credentials. See: https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token",
    "not_found": "The server indicated no data was found.",
    "unsupported": "The request is not supported.",
    "unknown": "An unknown error occurred.",
    "valid": "The request returned successfully, but an unknown exception occurred.",
}


def debug_requests_on():
    """ Turn on the logging for requests """
    logger = logging.getLogger(__name__)
    try:
        from http.client import HTTPConnection

        HTTPConnection.set_debuglevel(HTTPConnection, 1)
    except ImportError:
        import httplib

        httplib.HTTPConnection.debuglevel = 2

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


def convert_datetime(date, date_format="%Y-%m-%d"):
    """ Safely convert a date string to datetime """
    try:
        # try to turn the string into a date-time object
        tmp_date = datetime.strptime(date, date_format)
    except ValueError:  # ValueError will be thrown if format is invalid
        secho(
            "Invalid date: " + date + " must be yyyy-mm-dd", fg="bright_red",
        )
        return None
    return tmp_date


def get_date(date):
    """ Finds the date info in a string """
    prefix = ""
    if (">" or "=" or "<") in date[0]:
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


def get_valid_request(url, auth=""):
    """
    Provide a URL to submit a GET request for and handle a connection error or raise an assertion error if an HTTP status code indicating anything other than a success was received.
    """
    try:
        session = requests.Session()
        if auth:
            session.auth = (auth.split(":")[0], auth.split(":")[1])
        request = session.get(url)
    except requests.exceptions.ConnectionError:
        secho("Internet connection error...", fg="bright_red")
        return None

    if not request.status_code in (200, 202):
        raise requests.exceptions.HTTPError(f"HTTP Status Code: {request.status_code}")
    return request


def search_error(status_code):
    """
    This returns a directive on how to handle a given HTTP status code.
    """
    int_status_code = int(
        status_code
    )  # Need to make sure the status code is an integer

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
    except KeyError as ke:
        return "unsupported"


def search(
    language=None,
    created=None,
    pushed=None,
    stars=">=100",
    topics=[],
    user=None,
    debug=False,
    order="desc",
    auth="",
):
    """ Returns repositories searched from GitHub API """
    date_format = "%Y-%m-%d"  # date format in iso format
    if debug:
        debug_requests_on()
        print("DEBUG: search: created param:", created)
        print("DEBUG: search: order param: ", order)

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

    if user:
        query = f"user:{user}+"
    else:
        query = ""

    query += f"stars:{stars}+created:{created_str}"  # construct query
    query += f"+pushed:{pushed_str}"  # add pushed info to query
    query += f"+language:{language}" if language else ""  # add language to query
    query += f"".join(["+topic:" + i for i in topics])  # add topics to query

    url = f"{API_URL}?q={query}&sort=stars&order={order}"  # use query to construct url
    if debug:
        print("DEBUG: search: url:", url)  # print the url when debugging

    if debug and auth:
        print("DEBUG: auth: on")
    elif debug:
        print("DEBUG: auth: off")

    request = get_valid_request(url, auth)
    if request is None:
        return request

    return request.json()["items"]


def search_github_trending(
    language=None, spoken_language=None, order="desc", stars=">=10", date_range=None
):
    """ Returns trending repositories from github trending page """
    url = "https://github.com/trending?"  # filter for spoken language is available only here
    if language:
        url += f"language={language}"  # filter by programming language
    if spoken_language:
        url += f"&spoken_language_code={spoken_language}"  # filter by spoken language
    if date_range:
        url += f"&since={date_range_map[date_range]}"

    request = get_valid_request(url)
    if request is None:
        return request

    page = request.text

    soup = BeautifulSoup(page, "lxml")
    repo_list = soup.find_all("article", class_="Box-row")
    repositories = []
    for repo in repo_list:
        repo_dict = {}
        repo_dict["full_name"] = repo.h1.a.text.replace(" ", "").replace("\n", "")
        repo_dict["name"] = repo_dict["full_name"].split("/")[1]
        repo_dict["html_url"] = f"https://github.com/{repo_dict['full_name']}"
        div = repo.find("div", class_="f6 text-gray mt-2")
        anchor_list = div.find_all("a")
        span_list = div.find_all("span")
        # if stars present
        repo_dict["stargazers_count"] = (
            int(anchor_list[0].text.strip().replace(",", ""))
            if anchor_list[0].text
            else -1
        )
        # if forks count present
        repo_dict["forks_count"] = (
            int(anchor_list[1].text.strip().replace(",", ""))
            if anchor_list[1].text
            else -1
        )
        # if language is present
        language_span = div.span.find_all("span")
        if len(language_span) > 0:
            if (
                not language or language_span[1].text.strip().lower() == language
            ):  # if major lang of repo is same as language
                repo_dict["language"] = language_span[1].text.strip()
            else:
                repo_dict["language"] = language
        else:
            repo_dict["language"] = None
        # if description is present
        repo_dict["description"] = repo.p.text.strip() if repo.p else None
        # if stars date range is present
        if date_range:
            repo_dict["date_range"] = (
                span_list[-1].text.replace("\n", "").strip()
                if len(span_list) > 0
                else None
            )
        else:
            repo_dict["date_range"] = None
        repo_dict["watchers_count"] = -1  # watchers count not available
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
