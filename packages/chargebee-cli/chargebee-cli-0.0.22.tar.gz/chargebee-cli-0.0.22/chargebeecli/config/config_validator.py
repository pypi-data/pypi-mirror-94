from chargebeecli.constants.constants import ACTIVE_PROFILE_SECTION_NAME, API_KEY_NAME, ACCOUNT_KEY_NAME
from chargebeecli.constants.error_messages import NO_ACTIVE_PROFILE, ACCOUNT_API_NOT_SET
from chargebeecli.util.printer_util import custom_print


def validate_account_api_key(config):
    if config.has_section(ACTIVE_PROFILE_SECTION_NAME) is not True:
        custom_print(NO_ACTIVE_PROFILE, err=True)
        exit()
    configured_active_profile = config.get(ACTIVE_PROFILE_SECTION_NAME, 'primary')

    if config.has_section(configured_active_profile):
        if config.has_section(configured_active_profile):
            if (config.get(configured_active_profile, API_KEY_NAME) and config.get(configured_active_profile,
                                                                                   ACCOUNT_KEY_NAME)) is not None:
                return True
            else:
                custom_print(ACCOUNT_API_NOT_SET, err=True)
                exit()

        else:
            custom_print(ACCOUNT_API_NOT_SET, err=True)
            exit()

    else:
        custom_print(ACCOUNT_API_NOT_SET, err=True)
        exit()

