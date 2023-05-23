"""tests.test_search"""

from datetime import datetime, timedelta
from random import randint

import pytest

from starcli.search import search, search_github_trending


def test_search_language():
    """Test searching by language"""
    for language in ["python", "Python", "JavaScript", "c"]:
        repos = search([language])
        for repo in repos:
            assert repo["stargazers_count"] >= 0
            assert repo["forks"] >= 0
            assert repo["language"].lower() == language.lower()
            assert (repo["description"] is None) or repo["description"]
            assert repo["full_name"].count("/") == 1
            assert repo["full_name"] == f"{repo['owner']['login']}/{repo['name']}"
            assert repo["html_url"] == "https://github.com/" + repo["full_name"]


def test_search_topics():
    """Test searching by topics"""
    for topics in [
        "deezer",
        "django",
        "cookiecutter",
        ["web", "flask"],
        "python3",
        "algorithm",
        "shell",
    ]:
        repos = search(languages=["python"], topics=topics)
        for repo in repos:
            assert repo["stargazers_count"] >= 0
            assert repo["forks"] >= 0
            assert repo["language"].lower() == "python"
            assert (repo["description"] is None) or repo["description"]
            assert repo["full_name"].count("/") >= 1
            assert repo["full_name"] == f"{repo['owner']['login']}/{repo['name']}"
            assert repo["html_url"] == "https://github.com/" + repo["full_name"]
            assert topics in repo["topics"]


def test_search_created_date():
    """Test searching with creation date"""
    date_format = "%Y-%m-%d"
    day_range = 0 - randint(100, 400)
    created_date_value = (datetime.utcnow() + timedelta(days=day_range)).strftime(
        date_format
    )
    repos = search(languages=["python"], created=created_date_value)
    for repo in repos:
        assert repo["stargazers_count"] >= 0
        assert repo["forks"] >= 0
        assert (repo["description"] is None) or repo["description"]
        assert repo["full_name"].count("/") >= 1
        assert repo["full_name"] == f"{repo['owner']['login']}/{repo['name']}"
        assert repo["html_url"] == "https://github.com/" + repo["full_name"]

        assert datetime.strptime(
            repo["created_at"].split("T")[0], date_format
        ) >= datetime.strptime(created_date_value, date_format) and datetime.strptime(
            repo["created_at"].split("T")[0], date_format
        ) <= datetime.strptime(
            created_date_value, date_format
        ) + timedelta(
            days=1
        )


def test_search_pushed_date():
    """Test searching with updated date"""
    date_format = "%Y-%m-%d"
    day_range = 0 - randint(100, 400)
    pushed_date_value = (datetime.utcnow() + timedelta(days=day_range)).strftime(
        date_format
    )
    repos = search(languages=["python"], pushed=pushed_date_value)
    for repo in repos:
        assert repo["stargazers_count"] >= 0
        assert repo["forks"] >= 0
        assert (repo["description"] is None) or repo["description"]
        assert repo["full_name"].count("/") >= 1
        assert repo["full_name"] == f"{repo['owner']['login']}/{repo['name']}"
        assert repo["html_url"] == "https://github.com/" + repo["full_name"]

        # Need to account for min and max updated dates
        assert datetime.strptime(
            repo["pushed_at"].split("T")[0], date_format
        ) >= datetime.strptime(pushed_date_value, date_format) and datetime.strptime(
            repo["pushed_at"].split("T")[0], date_format
        ) <= datetime.strptime(
            pushed_date_value, date_format
        ) + timedelta(
            days=1
        )


@pytest.mark.xfail(raises=AssertionError)
def test_search_stars():
    """Test searching with number of stars"""
    repos = search(languages=["python"], stars="<10")
    for repo in repos:
        # FIXME: Possibly problem with GitHub API?
        assert repo["stargazers_count"] < 10  # Somestimes stars+1
        assert repo["forks"] >= 0
        assert (repo["description"] is None) or repo["description"]
        assert repo["full_name"].count("/") >= 1
        assert repo["full_name"] == f"{repo['owner']['login']}/{repo['name']}"
        assert repo["html_url"] == "https://github.com/" + repo["full_name"]


def test_search_user():
    """Test searching by user"""
    repos = search(languages=["ruby"], user="octocat")
    for repo in repos:
        assert repo["stargazers_count"] >= 0
        assert repo["forks"] >= 0
        assert (repo["description"] is None) or repo["description"]
        assert repo["full_name"].split("/")[0] == "octocat"
        assert repo["full_name"] == f"{repo['owner']['login']}/{repo['name']}"
        assert repo["html_url"] == "https://github.com/" + repo["full_name"]


def test_no_results():
    """Test if no search results found"""
    repos = search(["python"], "2020-01-01", "2019-01-01")
    assert repos == []


# commented until upstream github trending dependency is fixed
@pytest.mark.xfail()
def test_spoken_language():
    """Test search by spoken languages"""
    repos = search_github_trending(["javascript"], "zh")  # zh = chinese
    for repo in repos:
        assert repo["stargazers_count"] >= 0
        assert repo["forks"] >= 0
        assert repo["language"].lower() == "javascript"
        assert (repo["description"] == None) or repo["description"]
        assert repo["full_name"].count("/") >= 1
        assert repo["html_url"] == "https://github.com/" + repo["full_name"]

@pytest.mark.xfail()
def test_date_range():
    """Test search by date range"""
    for date_range in ["daily", "monthly", "weekly"]:
        repos = search_github_trending(["python"], "en", date_range)
        for repo in repos:
            assert repo["stargazers_count"] >= 0
            assert repo["forks"] >= 0
            assert repo["language"].lower() == "python"
            assert (repo["description"] == None) or repo["description"]
            assert repo["full_name"].count("/") >= 1
            assert repo["html_url"] == "https://github.com/" + repo["full_name"]
            # TODO: verify date range


def test_search_multiple_language():
    """Test searching by multiple language"""
    languages = ["python", "c"]
    repos = search(languages)
    for repo in repos:
        assert repo["stargazers_count"] >= 0
        assert repo["forks"] >= 0
        assert repo["language"].lower() in languages
        assert (repo["description"] is None) or repo["description"]
        assert repo["full_name"].count("/") == 1
        assert repo["full_name"] == f"{repo['owner']['login']}/{repo['name']}"
        assert repo["html_url"] == "https://github.com/" + repo["full_name"]
