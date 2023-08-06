
DEFAULT_THEME_NAME = 'basic'
available_themes = [
    {
        'name': DEFAULT_THEME_NAME,
        'header-color': 'NOCOLOR',
        'data-color': 'NOCOLOR'

    },
    {
        'name': 'terminal',
        'header-color': 'GREEN',
        'data-color': 'CYAN'

    },
    {
        'name': 'homebrew',
        'header-color': 'GREEN',
        'data-color': 'GREEN'

    },
    {
        'name': 'ocean',
        'header-color': 'NOCOLOR',
        'data-color': 'GREEN'

    }
]

THEME_DISPLAY_DATA = {
    'header': ['column 1', 'column 2', 'column 3'],
    'data': [['hi!!!', ' from', 'developer'],
             ['thanks', 'for', 'using it'],
             ['please', 'provide', 'your feedback']],

}


def get_theme(name):
    for available_theme in available_themes:
        if available_theme['name'] == name:
            return available_theme
    return None


def get_default_theme():
    for available_theme in available_themes:
        if available_theme['name'] == DEFAULT_THEME_NAME:
            return available_theme

