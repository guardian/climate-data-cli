from rich import print

fg = {
    "cyan": "\033[1;36m",
    "yellow": "\033[1;33m",
    "blue": "\033[1;34m",
    "red": "\033[1;31m",
    "grey": "\033[1;90m",
    "white": "\033[0;37m",
    "green": "\033[1;32m",
    "purple": "\033[1;35m",
}

bg = {
    "cyan": "\033[1;46m",
    "yellow": "\033[1;43m",
    "blue": "\033[1;44m",
    "red": "\033[1;41m",
    "grey": "\033[0;100m",
    "white": "\033[0;47m",
    "green": "\033[1;42m",
    "purple": "\033[1;45m",
}

reset = "\033[0m"


def message(text: str, after="\n", before=""):
    print(f"{before}[[yellow]![/yellow]] {text}{after}", end="")


def success(text: str, after="\n", before=""):
    print(f"{before}[[green]![/green]] {text}{after}", end="")


def error(text: str, after="\n", before=""):
    print(f"{before}[[red]![/red]] {text}{after}", end="")


def color(color, text):
    if color not in fg:
        raise ValueError(f"'{color}' is not a valid color")

    return f"{fg[color]}{text}{reset}"


def badge(color, text):
    if color not in bg or color not in fg:
        raise ValueError(f"'{color}' is not a valid color")

    return f"{fg['white']}{bg[color]}{text}{reset}"


def highlighted_list(items):
    if type(items) is not list:
        if not type(items) is str:
            return color("green", f"{items}")
        else:
            return color("green", f'"{items}"')

    colored_items = [color("green", f'"{item}"') for item in items]

    return f"[{', '.join(colored_items)}]"
