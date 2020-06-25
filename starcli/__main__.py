""" starcli.__main__ """

from argparse import Namespace

# Internal application imports
from .list_layout import list_layout
from .table_layout import table_layout
from .search import search
from .parser import args


def cli(args={}):
    if args == {}:  # if args is not provided
        args = Namespace(lang=None, stars=None, date=None, debug=False)

    if not args.stars:  # if args.stars is not present
        args.stars = ">=50"
    tmp_repos = search(args.lang, args.date, args.stars, args.debug)
    if not tmp_repos:  # if search() returned None
        return

    repos = []
    for i in range(args.limit_results):
        repos.append(tmp_repos[i])

    if args.layout == "table":
        table_layout(repos)
        return
    list_layout(repos)


if __name__ == "__main__":
    cli(args)
