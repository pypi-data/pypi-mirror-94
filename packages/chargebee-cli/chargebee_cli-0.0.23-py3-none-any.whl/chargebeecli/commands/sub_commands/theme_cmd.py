import click

from chargebeecli.constants.constants import Formats, Export_Formats, ApiOperation
from chargebeecli.processors.themes.theme import Theme


@click.command("theme", help='[ themes for cli ]')
@click.pass_context
@click.option("--name", "-n", help="theme name", required=False, type=str)
@click.option("--operation", "-op", required=True,
              help=" operation to be executed, like /list/fetch/apply.. ")
def theme_cmd(ctx, name, operation):
    if operation == "apply":
        operation = ApiOperation.CREATE.value
    Theme(export_format=None, export_path=None, file_name=None,
          response_format=Formats.TABLE.value, _operation=operation, _input_columns=None) \
        .process(None, operation, payload=None, resource_id=name) \
        .print_response()
