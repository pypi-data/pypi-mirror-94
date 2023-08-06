from configparser import ConfigParser

FILE_PATH = 'chargebee.config'

config = ConfigParser()
config.read(FILE_PATH)


def get_config():
    config
