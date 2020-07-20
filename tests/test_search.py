""" tests.test_search """

from starcli.search import search
from datetime import datetime, timedelta


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
        assert (repo["description"] == None) or repo["description"]
        assert repo["full_name"].count("/") >= 1
        assert repo["html_url"] == "https://github.com/" + repo["full_name"]

def test_search_topics():
    """
    Test the search functionality for starcli.search.
    """
    repos = search(topics=["open", "source"])
    for repo in repos:
        assert repo["stargazers_count"] >= 0
        assert repo["watchers_count"] >= 0
        assert repo["forks_count"] >= 0
        assert (repo["description"] == None) or repo["description"]
        assert repo["full_name"].count("/") >= 1
        assert repo["html_url"] == "https://github.com/" + repo["full_name"]

def test_search_created_date():
    """
    Test the search functionality for starcli.search.
    """
    created_date_value = "2020-01-01"
    date_format = "%Y-%m-%d"
    repos = search(date_created=created_date_value)
    for repo in repos:
        assert repo["stargazers_count"] >= 0
        assert repo["watchers_count"] >= 0
        assert repo["forks_count"] >= 0
        assert (repo["description"] == None) or repo["description"]
        assert repo["full_name"].count("/") >= 1
        assert repo["html_url"] == "https://github.com/" + repo["full_name"]
        # Need to account for min and max created dates
        assert (datetime.strptime(repo["created_at"].split("T")[0], date_format) >= datetime.strptime(created_date_value, date_format) and datetime.strptime(repo["created_at"].split("T")[0], date_format) <= datetime.strptime(created_date_value, date_format) + timedelta(days=1))

def test_search_updated_date():
    """
    Test the search functionality for starcli.search.
    """
    updated_date_value = "2020-01-01"
    date_format = "%Y-%m-%d"
    repos = search(last_updated=updated_date_value)
    for repo in repos:
        assert repo["stargazers_count"] >= 0
        assert repo["watchers_count"] >= 0
        assert repo["forks_count"] >= 0
        assert (repo["description"] == None) or repo["description"]
        assert repo["full_name"].count("/") >= 1
        assert repo["html_url"] == "https://github.com/" + repo["full_name"]
        # Need to account for min and max updated dates
        assert (datetime.strptime(repo["updated_at"].split("T")[0], date_format) >= datetime.strptime(updated_date_value, date_format) and datetime.strptime(repo["updated_at"].split("T")[0], date_format) <= datetime.strptime(updated_date_value, date_format) + timedelta(days=1))

def test_search_stars():
    """
    Test the search functionality for starcli.search.
    """
    repos = search(stars="1")
    for repo in repos:
        assert repo["stargazers_count"] == 1
        assert repo["watchers_count"] >= 0
        assert repo["forks_count"] >= 0
        assert (repo["description"] == None) or repo["description"]
        assert repo["full_name"].count("/") >= 1
        assert repo["html_url"] == "https://github.com/" + repo["full_name"]

def test_no_results():
    """ Test if no search results found """
    repos = search("python", "2020-01-01", "2019-01-01")
    assert repos == []
