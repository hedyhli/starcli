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


def convert_datetime(date, date_format):
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


def search(
    language=None,
    date_created=None,
    last_updated=None,
    stars=">=100",
    topics=[],
    debug=False,
    order="desc",
):
    """ Returns repositories based on the language, date, and stars

    """
    date_format = "%Y-%m-%d"  # date format in iso format
    if debug:
        debug_requests_on()
        print("DEBUG: search: date_created param:", date_created)
        print("DEBUG: search: order param: ", order)

    day_range = 0 - randint(100, 400)  # random negative from 100 to 400

    if not date_created:  # if date_created not provided
        # creation date: start, is the time now minus a random number of days
        # 100 to 400 days - which was stored in day_range
        start_date_created = (datetime.utcnow() + timedelta(days=day_range)).strftime(
            date_format
        )
        end_date_created = (datetime.utcnow() + timedelta(days=1)).strftime(date_format)
    else:  # if date_created is provided
        tmp_date = convert_datetime(date_created, date_format)
        if tmp_date is None:
            return None
        end_date_created = (tmp_date + timedelta(days=1)).strftime(date_format)
        start_date_created = tmp_date.strftime(date_format)

    if not last_updated:  # if last_updated not provided
        # update date: start, is the time now minus a random number of days
        # 100 to 400 days - which was stored in day_range
        start_last_updated = (datetime.utcnow() + timedelta(days=day_range)).strftime(
            date_format
        )
        end_last_updated = (datetime.utcnow() + timedelta(days=1)).strftime(date_format)
    else:  # if last_updated is provided
        tmp_date = convert_datetime(last_updated, date_format)
        if tmp_date is None:
            return None
        end_last_updated = (tmp_date + timedelta(days=1)).strftime(date_format)
        start_last_updated = tmp_date.strftime(date_format)

    if debug:  # print start_date and end_date if debugging
        print("DEBUG: search: start_date_created:", start_date_created)
        print("DEBUG: search: end_date_created:", end_date_created)
        print("DEBUG: search: start_last_updated:", start_last_updated)
        print("DEBUG: search: end_last_updated:", end_last_updated)

    query = f"stars:{stars}+created:{start_date_created}..{end_date_created}"  # construct query
    query += (
        f"+pushed:{start_last_updated}..{end_last_updated}"  # add last updated to query
    )
    query += f"+language:{language}" if language else ""  # add language to query
    query += f"".join(["+topic:" + i for i in topics])  # add topics to query

    url = f"{API_URL}?q={query}&sort=stars&order={order}"  # use query to construct url
    if debug:
        print("DEBUG: search: url:", url)  # print the url when debugging

    try:
        repositories = requests.get(url).json()  # get the response using the url
    except requests.exceptions.ConnectionError:
        secho("Internet connection error...", fg="bright_red")
        return None

    return repositories["items"]


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
    try:
        page = requests.get(url).text
    except requests.exceptions.ConnectionError:
        secho("Internet connection error...", fg="bright_red")
        return None

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
