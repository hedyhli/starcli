""" starcli.search """

# Standard library imports
from datetime import datetime, timedelta

# Third party imports
import requests


API_URL = "https://api.github.com/search/repositories"


def search(language=None, date=None, stars=">=50", debug=False, order="desc"):
    """ Returns repositories based on the language.
        repositories are sorted by stars
    """
    date_format = "%Y-%m-%d"  # date format in iso format
    if debug:
        print("DEBUG: search: date param:", date)
        print("DEBUG: search: order param: ", order)

    if not date:
        start_date = (datetime.utcnow() + timedelta(days=-100)).strftime(date_format)
        end_date = (datetime.utcnow() + timedelta(days=1)).strftime(date_format)
    else:
        try:
            tmp_date = datetime.strptime(date, date_format)
        except ValueError:
            print("invalid date format: " + date + " must be yyyy-mm-dd")
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

    repositories = requests.get(url).json()

    return repositories["items"]
