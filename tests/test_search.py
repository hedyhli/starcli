""" tests.test_search """

from starcli.search import search, search_github_trending


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


def test_no_results():
    """ Test if no search results found """
    repos = search("python", "2020-01-01", "2019-01-01")
    assert repos == []


def test_spoken_language():
    """ Test search by spoken_languages """
    repos = search_github_trending("javascript", "zh")  # zh = chinese
    for repo in repos:
        assert repo["stargazers_count"] >= 0 or repo["stargazers_count"] == -1
        assert repo["forks_count"] >= 0 or repo["forks_count"] == -1
        assert repo["language"].lower() == "javascript"
        assert (repo["description"] == None) or repo["description"]
        assert repo["full_name"].count("/") >= 1
        assert repo["html_url"] == "https://github.com/" + repo["full_name"]
