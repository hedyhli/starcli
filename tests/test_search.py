""" tests.test_search """

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


def test_no_results():
    """ Test if no search results found """
    repos = search("python", "2020-01-01", "2019-01-01")
    assert repos == []
