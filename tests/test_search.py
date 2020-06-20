""" tests.test_search """

from starcli.search import search


def test_search():
    """ Test the search function from starcli.search """
    repos = search("python")
    for repo in repos:
        assert repo["stargazers_count"] >= 0
        assert repo["watchers_count"] >= 0
        assert repo["forks_count"] >= 0
        assert repo["language"].lower() == "python"
        assert (repo["description"] == None) or repo["description"]
        assert repo["full_name"].count("/") >= 1
        assert repo["html_url"] == "https://github.com/" + repo["full_name"]
