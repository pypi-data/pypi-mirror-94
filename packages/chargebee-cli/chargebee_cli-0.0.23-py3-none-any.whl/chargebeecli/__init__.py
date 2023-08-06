from configparser import ConfigParser

import click

FILE_PATH = 'chargebee.config'

config = ConfigParser()
config.read(FILE_PATH)


def get_config():
    click.echo("testtttttt")
    click.echo(len(config))
    config
