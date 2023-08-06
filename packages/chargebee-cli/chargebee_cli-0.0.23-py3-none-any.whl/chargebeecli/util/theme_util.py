from chargebeecli.config.Configuration import Configuration
from chargebeecli.constants.constants import ACTIVE_THEME_SECTION_NAME
from chargebeecli.processors.themes.available_themes import get_default_theme, get_theme


def get_active_theme():
    section = Configuration.Instance().is_section_exist(ACTIVE_THEME_SECTION_NAME, "theme")
    if section is None:
        return get_default_theme()
    else:
        return get_theme(section)
