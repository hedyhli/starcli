""" starcli.__main__ """

# Internal application imports
from .list_layout import list_layout
from .table_layout import table_layout
from .search import search
from .parser import args


def cli(args):
    if not args.stars:  # if args.stars is not present
        args.stars = ">=50"
    repos = search(args.lang, args.date, args.stars, args.debug)
    if args.layout == "table":
        table_layout(repos)
        return
    list_layout(repos)


if __name__ == "__main__":
    cli(args)
