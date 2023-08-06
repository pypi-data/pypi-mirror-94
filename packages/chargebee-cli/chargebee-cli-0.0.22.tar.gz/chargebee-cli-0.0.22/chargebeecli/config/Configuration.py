import os
import shutil
from configparser import ConfigParser, NoSectionError

from chargebeecli.config.config_validator import validate_account_api_key
from chargebeecli.constants.constants import ACTIVE_PROFILE_SECTION_NAME, API_KEY_NAME, ACCOUNT_KEY_NAME


class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Other than that, there are
    no restrictions that apply to the decorated class.

    To get the singleton instance, use the `Instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    Limitations: The decorated class cannot be inherited from.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def Instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)


@Singleton
class Configuration:

    def __init__(self):
        user_config_dir = os.path.expanduser("~") + "/.chargebee"
        user_config = user_config_dir + "/config"
        if not os.path.isfile(user_config):
            path = os.path.abspath(os.path.dirname(__file__))
            os.makedirs(user_config_dir, exist_ok=True)
            shutil.copyfile(path + "/default_config.ini", user_config)
        self.config_path = user_config
        self.config = ConfigParser()
        self.config.read(f"{user_config_dir}/config")

    def fetch_available_sections(self):
        return self.config.sections()

    def delete_section_or_profile(self, __section):
        return self.config.remove_section(__section)

    def fetch_section(self, __profile, item_key):
        return self.config.get(__profile, item_key)

    def is_section_exist(self, __profile, item_key):
        try:
            return self.config.get(__profile, item_key)
        except NoSectionError as e:
            return None

    def get_account_api_key(self):
        validate_account_api_key(self.config)
        configured_active_profile = self.config.get(ACTIVE_PROFILE_SECTION_NAME, 'primary')
        return {API_KEY_NAME: self.config.get(configured_active_profile, API_KEY_NAME)
            , ACCOUNT_KEY_NAME: self.config.get(configured_active_profile, ACCOUNT_KEY_NAME)}

    def add_section(self, section, values):
        self.config.add_section(section)
        for key, val in values.items():
            self.config.set(section, key, val)
        with open(self.config_path, 'w') as f:
            self.config.write(f)

    def update_section(self, section, values):
        if self.config.has_section(section):
            for key, val in values.items():
                self.config.set(section, key, val)
        else:
            self.add_section(section, values)

        with open(self.config_path, 'w') as f:
            self.config.write(f)
