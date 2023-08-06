import click

from chargebeecli.constants.constants import Formats, Export_Formats
from chargebeecli.processors.subs.subscriptions import Subscription
from chargebeecli.util.multiple_columns import MultipleColumns
from chargebeecli.util.theme_util import get_active_theme


@click.command(name="subs", help='endpoint to perform operation on [subscription] resource')
@click.pass_context
@click.option("--id", "-i", help="subscription id", required=False, type=str)
@click.option("--operation", "-op", required=True,
              help=" operation to be executed, like fetch/create/update/delete.. ")
@click.option("--format", "-f", required=False,
              help="this allows user to format the output in json or table format..", default=Formats.TABLE.name,
              show_default=True)
@click.option('--columns-subs', "-s", nargs=-1, required=False, help="columns to be printed in output",
              cls=MultipleColumns)
@click.option('--columns-cus', "-c", nargs=-1, required=False, help="columns to be printed in output",
              cls=MultipleColumns)
@click.option('--export-format', "-ef", help='data to be imported in [csv / excel / html',
              default=Export_Formats.CSV.value, type=str)
@click.option('--export-filename', "-efn", help='name of exported file', type=str)
@click.option('--export-path', "-ep", help='path where file to be exported', type=click.Path(exists=True))
def cmd(ctx, id, operation, columns_subs, columns_cus, format, export_filename, export_format, export_path):

    Subscription(columns_subs=columns_subs, columns_customer=columns_cus, _operation=operation, export_format=export_format,
                 export_path=export_path, file_name=export_filename, response_format=format) \
        .validate_param() \
        .process(None, operation, payload=None, resource_id=id) \
        .format() \
        .export_data() \
        .print_response(get_active_theme())
