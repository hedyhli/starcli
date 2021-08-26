""" starcli.search """

# Standard library imports
from datetime import datetime, timedelta
from time import sleep
import logging
from random import randint
import re
import os
import math
import github
from github import Github
import pandas as pd
import matplotlib.pyplot as plt

# Third party imports
import requests
from click import secho
import colorama
from gtrending import fetch_repos
import http.client
from rich.logging import RichHandler

API_URL = "https://api.github.com/search/repositories"

date_range_map = {
    "today": "daily",
    "this-week": "weekly",
    "this-month": "monthly"}

status_actions = {
    "retry": "Failed to retrieve data. Retrying in ",
    "invalid": "The server was unable to process the request.",
    "unauthorized": "The server did not accept the credentials. See: https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token",
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


def convert_datetime(date, date_format="%Y-%m-%d"):
    """Safely convert a date string to datetime"""
    try:
        # try to turn the string into a date-time object
        tmp_date = datetime.strptime(date, date_format)
    except ValueError:  # ValueError will be thrown if format is invalid
        secho(
            "Invalid date: " + date + " must be yyyy-mm-dd",
            fg="bright_red",
        )
        return None
    return tmp_date


def get_date(date):
    """Finds the date info in a string"""
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


def get_valid_request(url, auth=""):
    """
    Provide a URL to submit a GET request for and handle a connection error.
    """
    while True:
        try:
            session = requests.Session()
            if auth:
                session.auth = (auth.split(":")[0], auth.split(":")[1])
            request = session.get(url)
        except requests.exceptions.ConnectionError:
            secho("Internet connection error...", fg="bright_red")
            return None

        if request.status_code not in (200, 202):
            handling_code = search_error(request.status_code)
            if handling_code == "retry":
                for i in range(15, 0, -1):
                    secho(
                        f"{status_actions[handling_code]} {i} seconds...",
                        fg="bright_yellow",
                    )  # Print and update a timer

                    sleep(1)
            elif handling_code in status_actions:
                secho(status_actions[handling_code], fg="bright_yellow")
                return None
            else:
                secho(
                    "An invalid handling code was returned.",
                    fg="bright_red")
                return None
        else:
            break

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
    except KeyError:
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
    """Returns repositories searched from GitHub API"""
    date_format = "%Y-%m-%d"  # date format in iso format
    if debug:
        debug_requests_on()
        logger = logging.getLogger(__name__)
        logger.debug("Search: created param:" + created)
        logger.debug("Search: order param: " + order)

    day_range = 0 - randint(100, 400)  # random negative from 100 to 400

    if not created:  # if created not provided
        # creation date: the time now minus a random number of days
        # 100 to 400 days - which was stored in day_range
        created_str = ">=" + (datetime.utcnow() +
                              timedelta(days=day_range)).strftime(date_format)
    else:  # if created is provided
        created_str = get_date(created)
        if not created_str:
            return None

    if not pushed:  # if pushed not provided
        # pushed date: start, is the time now minus a random number of days
        # 100 to 400 days - which was stored in day_range
        pushed_str = ">=" + (datetime.utcnow() +
                             timedelta(days=day_range)).strftime(date_format)
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
    # add language to query
    query += f"+language:{language}" if language else ""
    query += f"".join(["+topic:" + i for i in topics])  # add topics to query

    # use query to construct url
    url = f"{API_URL}?q={query}&sort=stars&order={order}"
    if debug:
        logger.debug("Search: url:" + url)  # print the url when debugging
    if debug and auth:
        logger.debug("Auth: on")
    elif debug:
        logger.debug("Auth: off")

    request = get_valid_request(url, auth)
    if request is None:
        return request

    return request.json()["items"]


def search_github_trending(
        language=None,
        spoken_language=None,
        order="desc",
        stars=">=10",
        date_range=None):
    """Returns trending repositories from github trending page"""
    if date_range:
        gtrending_repo_list = fetch_repos(
            language, spoken_language, date_range_map[date_range]
        )
    else:
        gtrending_repo_list = fetch_repos(language, spoken_language)
    repositories = []
    for gtrending_repo in gtrending_repo_list:
        repo_dict = convert_repo_dict(gtrending_repo)
        repo_dict["date_range"] = (
            str(repo_dict["date_range"]) + " stars " + date_range.replace("-", " ")
            if date_range
            else None
        )
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
    return sorted(
        repositories,
        key=lambda repo: repo["stargazers_count"],
        reverse=True)


def draw_stargraph(reponame, auth, path, duration=""):
    g = Github()
    try:
        repo = g.get_repo(reponame)
        dictnry = dict()
        request_header = {'Accept': 'application/vnd.github.v3.star+json'}

        for pages in range(1, math.ceil(repo.stargazers_count / 30) + 1):
            # requesting the repo information via github REST API
            request = 'https://api.github.com/repos/{}/stargazers?page={}'.format(
                reponame, pages)

            r = requests.get(
                request,
                auth=(
                    auth.split(":")[0],
                    auth.split(":")[1]),
                headers=request_header)

            for items in r.json():
                items['starred_at'] = items['starred_at'].replace(
                    'T', " ")  # cleaning the collected dates
                items['starred_at'] = items['starred_at'].replace('Z', " ")

                # Converting to Year-Month format
                month = '{:%Y-%m}'.format(
                    datetime.strptime(
                        items['starred_at'].split(" ")[0],
                        '%Y-%m-%d'))
                # Adding the star counts monthly for each year
                if month not in dictnry.keys():
                    dictnry[month] = 1
                else:
                    dictnry[month] += 1

        for i in range(len(dictnry.keys())
                       ):  # arranging the star counts cummulatively over the time period
            if i >= 1:
                dictnry[list(dictnry.keys())[i]] = dictnry[list(dictnry.keys())[
                    i - 1]] + dictnry[list(dictnry.keys())[i]]

        data = pd.DataFrame(dictnry.items(), columns=['Year_Month', 'stars'])
        if duration == "yearly":
            data['Year_Month'] = pd.to_datetime(data['Year_Month'])
        data = data.set_index('Year_Month')

        # Plotting the star counts over the time period collected from the API
        fig, ax = plt.subplots(
            figsize=(
                len(dictnry) // 2, len(dictnry) // 3), constrained_layout=True)
        ax.plot(
            data.index,
            data.stars,
            color='tab:orange',
            label='Stars Count')
        ax.set_xlabel('Year-Month', size=30)
        ax.set_ylabel('Stars', size=30)
        ax.set_title('Stargazers', size=30)
        plt.xticks(rotation=90)
        ax.grid(True)
        plt.yticks(fontsize=30)
        plt.xticks(fontsize=25)
        if max(dictnry.values()) < 1000:
            fontsize = 10
        else:
            fontsize = 20
        for a, b in zip(data.index, data.stars):
            plt.text(
                a,
                b,
                str(b),
                verticalalignment='bottom',
                horizontalalignment='right',
                color='black',
                fontsize=fontsize)
        ax.legend(loc='upper left')
        plt.savefig(os.path.join(path, "output.png"))
        plt.close()
    except github.UnknownObjectException as e:
        if e.status == 404:
            print("Repository Not found")


def convert_repo_dict(gtrending_repo):
    repo_dict = {}
    repo_dict["full_name"] = gtrending_repo.get("fullname")
    repo_dict["name"] = gtrending_repo.get("name")
    repo_dict["html_url"] = gtrending_repo.get("url")
    repo_dict["stargazers_count"] = gtrending_repo.get("stars", -1)
    repo_dict["language"] = gtrending_repo.get("language")
    # gtrending_repo has key `description` and value is empty string if it's
    # empty
    repo_dict["description"] = (
        gtrending_repo.get("description")
        if gtrending_repo.get("description") != ""
        else None
    )
    repo_dict["date_range"] = gtrending_repo.get("currentPeriodStars")
    return repo_dict
