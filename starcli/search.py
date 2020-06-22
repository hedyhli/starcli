""" starcli.search """

# Standard library imports
from datetime import datetime, timedelta

# Third party imports
import requests
from rich.console import Console


API_URL = "https://api.github.com/search/repositories"
console = Console()


def search(language=None, date=None, stars=">=50", debug=False):
    """ Returns repositories based on the language.
        repositories are sorted by stars
    """

    if not date:
        start_date = datetime.fromisoformat(
            (datetime.utcnow() + timedelta(days=-100)).date().isoformat()
        )  # today's timestamp -100 days in YYYY-MM-DD:00:00:00 format
        end_date = datetime.fromisoformat(
            (datetime.utcnow() + timedelta(days=1)).date().isoformat()
        )  # next day's timestamp in YYYY-MM-DD:00:00:00 format
    else:
        start_date = datetime.fromisoformat(date)
        end_date = datetime.fromisoformat(
            (start_date + timedelta(days=1)).date().isoformat()
        )

    if debug:  # print start_date and end_date if debugging
        print("DEBUG: search: start date:", start_date)
        print("DEBUG: search: end_date:", end_date)

    query = f"stars:{stars}+created:{start_date.isoformat()}..{end_date.isoformat()}"
    query += f"+language:{language}" if language else ""
    url = f"{API_URL}?q={query}&sort=stars&order=desc"
    repositories = requests.get(url).json()

    if debug:
        print("DEBUG: search: url:", url)  # print the url when debugging
    return repositories["items"]
