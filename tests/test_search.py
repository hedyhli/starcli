""" tests.test_search """

from datetime import datetime, timedelta
from random import randint
from starcli.search import search


def test_search():
    """ Test the search functionality from starcli.search """
    repos = search("python")
    for repo in repos:
        assert repo["stargazers_count"] >= 0
        assert repo["watchers_count"] >= 0
        assert repo["forks_count"] >= 0
        assert repo["language"].lower() == "python"
        assert (repo["description"] is None) or repo["description"]
        assert repo["full_name"].count("/") >= 1
        assert repo["html_url"] == "https://github.com/" + repo["full_name"]


def test_search_topic():
    """ Test the search functionality from starcli.search """
    repos = search(language="python", topics=["deezer"])
    for repo in repos:
        assert repo["stargazers_count"] >= 0
        assert repo["watchers_count"] >= 0
        assert repo["forks_count"] >= 0
        assert repo["language"].lower() == "python"
        assert (repo["description"] is None) or repo["description"]
        assert repo["full_name"].count("/") >= 1
        assert repo["html_url"] == "https://github.com/" + repo["full_name"]


def test_search_topics():
    """
    Test the search functionality for starcli.search.
    """
    repos = search(language="python", topics=["open", "source"])
    for repo in repos:
        assert repo["stargazers_count"] >= 0
        assert repo["watchers_count"] >= 0
        assert repo["forks_count"] >= 0
        assert (repo["description"] is None) or repo["description"]
        assert repo["full_name"].count("/") >= 1
        assert repo["html_url"] == "https://github.com/" + repo["full_name"]


def test_search_created_date():
    """
    Test the search functionality for starcli.search.
    """
    date_format = "%Y-%m-%d"
    day_range = 0 - randint(100, 400)
    created_date_value = (datetime.utcnow() + timedelta(days=day_range)).strftime(
        date_format
    )
    repos = search(language="python", date_created=created_date_value)
    for repo in repos:
        assert repo["stargazers_count"] >= 0
        assert repo["watchers_count"] >= 0
        assert repo["forks_count"] >= 0
        assert (repo["description"] is None) or repo["description"]
        assert repo["full_name"].count("/") >= 1
        assert repo["html_url"] == "https://github.com/" + repo["full_name"]

        # Need to account for min and max created dates
        repo_created_date = datetime.strptime(
            repo["created_at"].split("T")[0],
            date_format,  # Need to remove the time portion to avoid errors
        )

        assert repo_created_date >= datetime.strptime(created_date_value, date_format)


def test_search_updated_date():
    """
    Test the search functionality for starcli.search.
    """
    date_format = "%Y-%m-%d"
    day_range = 0 - randint(100, 400)
    updated_date_value = (datetime.utcnow() + timedelta(days=day_range)).strftime(
        date_format
    )
    repos = search(language="python", last_updated=updated_date_value)
    for repo in repos:
        assert repo["stargazers_count"] >= 0
        assert repo["watchers_count"] >= 0
        assert repo["forks_count"] >= 0
        assert (repo["description"] is None) or repo["description"]
        assert repo["full_name"].count("/") >= 1
        assert repo["html_url"] == "https://github.com/" + repo["full_name"]

        # Need to account for min and max updated dates
        repo_updated_date = datetime.strptime(
            repo["updated_at"].split("T")[0],
            date_format,  # Need to remove the time portion to avoid errors
        )

        assert repo_updated_date >= datetime.strptime(updated_date_value, date_format)


def test_search_stars():
    """
    Test the search functionality for starcli.search.
    """
    repos = search(language="python", stars="1")
    for repo in repos:
        assert repo["stargazers_count"] == 1
        assert repo["watchers_count"] >= 0
        assert repo["forks_count"] >= 0
        assert (repo["description"] is None) or repo["description"]
        assert repo["full_name"].count("/") >= 1
        assert repo["html_url"] == "https://github.com/" + repo["full_name"]


def test_no_results():
    """ Test if no search results found """
    repos = search("python", "2020-01-01", "2019-01-01")
    assert repos == []
