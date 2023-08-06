import click

from chargebeecli.constants.constants import Formats, Export_Formats
from chargebeecli.processors.profile.profile import Profile
from chargebeecli.util.theme_util import get_active_theme


@click.command("profile", help='manage credentials for local chargebee profiles')
@click.pass_context
@click.option("--operation", "-op", required=True, type=str)
@click.option("--name", "-n", help="profile name", required=False, type=str)
@click.option("--format", "-f", required=False,
              help="this allows user to format the output in json or table format..", default=Formats.TABLE.name)
@click.option('--columns', '-cols', nargs=0, required=False, help="columns to be printed in output")
@click.argument('columns', nargs=-1)
@click.option('--export-format', "-ef", help='data to be imported in [csv / excel / html',
              default=Export_Formats.CSV.value, type=str)
@click.option('--export-filename', "-efn", help='name of exported file', type=str)
@click.option('--export-path', "-ep", help='path where file to be exported', type=click.Path(exists=True))
def cmd(ctx, operation, columns, format, name, export_filename, export_format, export_path):
    Profile(export_format=export_format, export_path=export_path, file_name=export_filename,
            response_format=format, _operation=operation, _input_columns=columns) \
        .validate_param() \
        .process(None, operation, payload=None, resource_id=name) \
        .format() \
        .export_data() \
        .print_response(get_active_theme())
