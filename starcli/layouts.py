""" starcli.layouts """

# Standard library imports
import textwrap
import math
from shutil import get_terminal_size

# Third party imports
from rich.align import Align
from rich.console import Console, group
from rich.rule import Rule
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich.columns import Columns

console = Console()

SYMBOL_MAP = {"stars": "★", "forks": "⎇"}


def shorten_count(number):
    """Shortens number"""
    if number < 1000:
        return str(number)

    number = int(number)
    new_number = math.ceil(round(number / 100.0, 1)) * 100

    if new_number % 1000 == 0:
        return str(new_number)[0] + "k"
    if new_number < 1000:
        # returns the same old integer if no changes were made
        return str(number)
    else:
        # returns a new string if the number was shortened
        return str(new_number / 1000.0) + "k"


def get_stats(repo):
    """return formatted string of repo stats"""
    stats = (
        f"{repo['stargazers_count']}{SYMBOL_MAP['stars']} "
        if repo["stargazers_count"] != "-1"
        else ""
    )
    stats += f"{repo['forks']}{SYMBOL_MAP['forks']} " if repo["forks"] != "-1" else ""
    return stats


def get_date_range(date_range):
    if not date_range:
        return Text("")
    return (
        Text("(", style="reset")
        .append(
            (date_range.replace(" stars", SYMBOL_MAP["stars"])), style="italic magenta"
        )
        .append(")")
    )


def list_layout(repos):
    """Displays repositories in list layout using rich"""

    LAYOUT_WIDTH = 80

    @group()
    def render_repo(repo):
        """Yields renderables for a single repo."""
        yield Rule(style="bright_yellow")
        yield ""
        # Table with description and stats
        title_table = Table.grid(padding=(0, 1))
        title_table.expand = True
        title = Text(repo["full_name"], overflow="fold")
        title.stylize(f"yellow link {repo['html_url']}")

        stats = get_stats(repo)
        date_range_col = get_date_range(repo.get("date_range"))

        title_table.add_row(title, Text(stats, style="italic blue"))
        title_table.columns[1].no_wrap = True
        title_table.columns[1].justify = "right"
        yield title_table
        yield ""
        lang_table = Table.grid(padding=(0, 1))
        lang_table.expand = True
        language_col = (
            Text(repo["language"], style="bold cyan")
            if repo["language"]
            else Text("no language")
        )
        lang_table.add_row(language_col, date_range_col)
        lang_table.columns[1].justify = "right"
        yield lang_table
        yield ""
        # Descripion
        description = repo["description"]
        if description:
            yield Text(description.strip())
        else:
            yield "[i]no description"
        yield ""

    def column(renderable):
        """Constrain width and align to center to create a column."""
        return Align.center(renderable, width=LAYOUT_WIDTH, pad=False)

    for repo in repos:
        console.print(column(render_repo(repo)))
    console.print(column(Rule(style="bright_yellow")))


def table_layout(repos):
    """Displays repositories in a table format using rich"""

    table = Table(leading=1)

    # make the columns
    table.add_column("Name", style="bold yellow")
    table.add_column("Language")
    table.add_column("Description")
    table.add_column("Stats", justify="right")

    for repo in repos:
        stats = Text(get_stats(repo), style="blue")
        stats.append("\n").append(get_date_range(repo.get("date_range")))

        language = (
            Text(repo["language"], style="cyan")
            if repo["language"]
            else Text("no language", style="italic")
        )
        description = (
            Text(repo["description"])
            if repo["description"]
            else Text("no description", style="italic")
        )

        name = Text(repo["name"], overflow="fold")
        name.stylize(f"yellow link {repo['html_url']}")

        table.add_row(name, language, description, stats)

    console.print(table)


def grid_layout(repos):
    """Displays repositories in a grid format using rich"""

    max_desc_len = 90

    panels = []
    for repo in repos:

        stats = get_stats(repo)
        # '\n' added here as it would group both text and new line together
        # hence if date_range isn't present the new line will also not be displayed
        date_range = get_date_range(repo.get("date_range")).append("\n")

        language = (
            Text(repo["language"], style="cyan")
            if repo["language"]
            else Text("no language", style="italic")
        )
        description = (
            Text(repo["description"])
            if repo["description"]
            else Text("no description", style="italic")
        )

        name = Text(repo["name"], style="bold yellow")
        name.stylize(f"link {repo['html_url']}")
        stats = Text(stats, style="blue")

        # truncate rest of the description if
        # it's more than 90 (max_desc_len) chars
        # using truncate() is better than textwrap
        # because it also takes care of asian characters
        description.truncate(max_desc_len, overflow="ellipsis")

        repo_summary = Text.assemble(
            name,
            "\n",
            stats,
            " ",
            date_range,
            language,
            "\n",
            description,
        )
        panels.append(Panel(repo_summary, expand=True))

    console.print((Columns(panels, width=30, expand=True)))


def print_results(*args, page=False, layout=""):
    """Use a specified layout to print or page the fetched results"""
    if page:
        with console.pager():
            print_layout(layout=layout, *args)
    else:
        print_layout(
            layout=layout,
            *args,
        )


def print_layout(*args, layout="list"):
    if layout == "table":
        table_layout(*args)
    elif layout == "grid":
        grid_layout(*args)
    else:
        list_layout(*args)
    return
