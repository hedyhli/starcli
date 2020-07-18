""" starcli.search """

# Standard library imports
from datetime import datetime, timedelta
import logging
from random import randint

# Third party imports
import requests
from click import echo, style
import colorama


API_URL = "https://api.github.com/search/repositories"


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
        echo(style("Invalid date: " + date + " must be yyyy-mm-dd", fg="bright_red",))
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
        echo(style("Internet connection error...", fg="bright_red"))
        return None

    return repositories["items"]
