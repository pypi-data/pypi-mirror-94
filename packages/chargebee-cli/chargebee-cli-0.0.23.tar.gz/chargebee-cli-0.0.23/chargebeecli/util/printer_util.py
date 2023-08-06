import click
from tabulate import tabulate

from chargebeecli.processors.themes.available_themes import THEME_DISPLAY_DATA, get_theme
from chargebeecli.util.COLORS import colors



def custom_print_themes(themes):
    for theme in themes:
        new_h = []
        for _h in THEME_DISPLAY_DATA['header']:
            new_h.append(colors[theme["theme"]["header-color"]] % _h)
        new_t = []
        for _t in THEME_DISPLAY_DATA['data']:
            tmp = []
            for __t in _t:
                tmp.append(colors[theme["theme"]["data-color"]] % __t)
            new_t.append(tmp)
        click.secho("---------------" + theme["theme"]["name"] + " ------------")
        click.secho(tabulate(new_t, new_h, tablefmt="grid", stralign="center", showindex=True), err=False, nl=True)
        click.secho("-----------------------------------------------------\n\n")


def custom_print(message, err=False):
    if err is not True:
        click.secho(message, fg='green', err=True, nl=True)
    else:
        click.secho('-----------------------------------', fg='white', err=False, nl=True)
        click.secho(message, fg='red', err=True, nl=True)
        click.secho('-----------------------------------', fg='white', err=False, nl=True)


def custom_print_table(tables, _headers, theme=None):
    new_h = []
    for _h in _headers:
        new_h.append(colors[theme["header-color"]] % _h)
    new_t = []
    for _t in tables:
        tmp = []
        for __t in _t:
            tmp.append(colors[theme["data-color"]] % __t)
        new_t.append(tmp)
    click.secho(tabulate(new_t, new_h, tablefmt="grid", stralign="center", showindex=True), err=False, nl=True)



