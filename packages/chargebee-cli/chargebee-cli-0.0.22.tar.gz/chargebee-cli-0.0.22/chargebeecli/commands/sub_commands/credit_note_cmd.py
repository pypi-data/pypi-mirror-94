import click

from chargebeecli.constants.constants import Formats, Export_Formats
from chargebeecli.processors.credit_notes.credit_note import CreditNote
from chargebeecli.util.theme_util import get_active_theme


@click.command("credit_note", help='endpoint to perform operation on [credit_note] resource')
@click.pass_context
@click.option("--id", "-i", help="credit_note id", required=False, type=str)
@click.option("--operation", "-op", required=True,
              help=" operation to be executed, like fetch/create/update/delete.. ")
@click.option('--columns', '-cols', nargs=0, required=False, help="columns to be printed in output")
@click.option("--format", "-f", required=False,
              help="this allows user to format the output in json or table format..", default=Formats.TABLE.name)
@click.argument('columns', nargs=-1)
@click.option('--export-format', "-ef", help='data to be imported in [csv / excel / html',
              default=Export_Formats.CSV.value, type=str)
@click.option('--export-filename', "-efn", help='name of exported file', type=str)
@click.option('--export-path', "-ep", help='path where file to be exported', type=click.Path(exists=True))
def cmd(ctx, id, operation, columns, format, export_filename, export_format, export_path):
    CreditNote(export_format=export_format, export_path=export_path, file_name=export_filename,
               response_format=format, _operation=operation, _input_columns=columns) \
        .validate_param() \
        .process(None, operation, payload=None, resource_id=id) \
        .format() \
        .export_data() \
        .print_response(get_active_theme())
