from chargebeecli.config.Configuration import Configuration
from chargebeecli.constants.constants import ACCOUNT_KEY_NAME
from chargebeecli.printer.printer import custom_print
from chargebeecli.util.url_validator import is_valid_url


def main():
    pass


def process(profile_name, profile_data):
    configuration = Configuration.Instance()
    if is_valid_url(profile_data[ACCOUNT_KEY_NAME]):
        configuration.update_section(profile_name, profile_data)
        custom_print("profile configured properly")
    else:
        custom_print(profile_data[ACCOUNT_KEY_NAME] + " :url is not valid", err=True)
        exit()


if __name__ == '__main__':
    main()
