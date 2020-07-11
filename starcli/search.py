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


def search(language=None, date_created=None, stars=">=100", debug=False, order="desc"):
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
        start_date = (datetime.utcnow() + timedelta(days=day_range)).strftime(
            date_format
        )
        end_date = (datetime.utcnow() + timedelta(days=1)).strftime(date_format)
    else:  # if date_created is provided
        try:
            # try to turn the string into a date-time object
            tmp_date = datetime.strptime(date_created, date_format)
        except ValueError:  # ValueError will be thrown if format is invalid
            echo(
                style(
                    "Invalid date: " + date_created + " must be yyyy-mm-dd",
                    fg="bright_red",
                )
            )
            return
        end_date = (tmp_date + timedelta(days=1)).strftime(date_format)
        start_date = tmp_date.strftime(date_format)

    if debug:  # print start_date and end_date if debugging
        print("DEBUG: search: start date:", start_date)
        print("DEBUG: search: end_date:", end_date)

    query = f"stars:{stars}+created:{start_date}..{end_date}"  # construct query
    query += f"+language:{language}" if language else ""  # add language to query
    url = f"{API_URL}?q={query}&sort=stars&order={order}"  # use query to construct url
    if debug:
        print("DEBUG: search: url:", url)  # print the url when debugging

    try:
        repositories = requests.get(url).json()  # get the response using the url
    except requests.exceptions.ConnectionError:
        echo(style("Internet connection error...", fg="bright_red"))
        return

    return repositories["items"]
