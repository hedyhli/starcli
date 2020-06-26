from argparse import ArgumentParser

parser = ArgumentParser(description="Browse trending repos on GitHub by stars")
parser.add_argument(
    "-l", "--lang", type=str, help="Language filter eg:python", required=False
)
parser.add_argument(
    "-d",
    "--date",
    type=str,
    help="Specify repo creation date in ISO8601 format YYYY-MM-DD",
    required=False,
)
parser.add_argument(
    "-L",
    "--layout",
    type=str,
    choices=("list", "table"),
    default="list",
    help="The output format (list or table), default is list",
)
parser.add_argument(
    "-s",
    "--stars",
    type=str,
    required=False,
    default=">=50",
    help="Range of stars required, default is '>=50'",
)
parser.add_argument(
    "-r",
    "--limit-results",
    type=int,
    default=7,
    help="Limit the number of results shown. Default: 7",
)
parser.add_argument(
    "-o",
    "--order",
    type=str,
    choices=("desc", "asc"),
    default="desc",
    help="Specify the order of repos by stars that is shown, 'desc' or 'asc', default: desc",
)
parser.add_argument("--debug", action="store_true", help="Turn on debugging mode")
args = parser.parse_args()
