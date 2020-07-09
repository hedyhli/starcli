""" starcli.search """

# Standard library imports
from datetime import datetime, timedelta
import logging

# Third party imports
import requests
from click import echo, style
import colorama


API_URL = "https://api.github.com/search/repositories"


def debug_requests_on():
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


def search(language=None, date=None, stars=">=50", debug=False, order="desc"):
    """ Returns repositories based on the language, date, and stars

    """
    date_format = "%Y-%m-%d"  # date format in iso format
    if debug:
        debug_requests_on()
        print("DEBUG: search: date param:", date)
        print("DEBUG: search: order param: ", order)

    if not date:
        start_date = (datetime.utcnow() + timedelta(days=-100)).strftime(date_format)
        end_date = (datetime.utcnow() + timedelta(days=1)).strftime(date_format)
    else:
        try:
            tmp_date = datetime.strptime(date, date_format)
        except ValueError:
            echo(
                style("Invalid date: " + date + " must be yyyy-mm-dd", fg="bright_red")
            )
            return
        end_date = (tmp_date + timedelta(days=1)).strftime(date_format)
        start_date = tmp_date.strftime(date_format)

    if debug:  # print start_date and end_date if debugging
        print("DEBUG: search: start date:", start_date)
        print("DEBUG: search: end_date:", end_date)

    query = f"stars:{stars}+created:{start_date}..{end_date}"
    query += f"+language:{language}" if language else ""
    url = f"{API_URL}?q={query}&sort=stars&order={order}"
    if debug:
        print("DEBUG: search: url:", url)  # print the url when debugging

    try:
        repositories = requests.get(url).json()
    except requests.exceptions.ConnectionError:
        echo(style("Internet connection error...", fg="bright_red"))
        return

    return repositories["items"]
