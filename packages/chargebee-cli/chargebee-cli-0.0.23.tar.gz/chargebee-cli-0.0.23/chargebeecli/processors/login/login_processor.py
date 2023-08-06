

from chargebeecli.config.Configuration import Configuration
from chargebeecli.constants.constants import ACTIVE_PROFILE_SECTION_NAME
from chargebeecli.printer.printer import custom_print


def process(profile):
    configuration = Configuration.Instance()
    if profile in configuration.fetch_available_sections():
        configuration.update_section(ACTIVE_PROFILE_SECTION_NAME, {'primary': profile})
        custom_print(f"{profile} active profile set")
    else:
        custom_print(f"{profile}: profile does not exist", err=True)
