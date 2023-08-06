import click
import pyfiglet

from .sub_commands import profile_cmd, plan_cmd, addon_cmd, coupon_cmd, address_cmd, card_cmd, comment_cmd, \
    coupon_code_cmd, coupon_set_cmd, credit_note_cmd, customer_cmd, event_cmd, gift_cmd, hosted_page_cmd, invoice_cmd, \
    order_cmd, promotional_credit_cmd, quote_cmd, subscription_cmd, transaction_cmd, unbilled_charge_cmd, theme_cmd
from ..constants.constants import API_KEY_NAME, ACCOUNT_KEY_NAME
from ..printer.printer import custom_print
from ..processors.login import login_processor
from ..processors.profile import profile_configurator


def safe_entry_point():
    entry_point()


# except Exception as e:
#     print(Fore.RED, '------------------------------------------')
#     print(Fore.RED, 'unable to process../ COMMAND NOT NOT FOUND',e)
#     print(Fore.RED, '------------------------------------------')
#     exit(0)

def get_cmd_help():
    return "------------------------------------------------------------------------\nunleash the power of chargebee " \
           "apis from your command prompt.					\n for api reference: " \
           "https://apidocs.chargebee.com/docs/api?prod_cat_ver=1 ] 	" \
           "\n-------------------------------------------------------------------------- "


@click.group(help=get_cmd_help())
@click.pass_context
def entry_point(ctx):
    """unleash the power of chargebee apis from your command prompt.
    for api reference: [ https://apidocs.chargebee.com/docs/api?prod_cat_ver=1 ]"""


# info cmd
@entry_point.command("info")
@click.pass_context
def info(ctx):
    """Get the information about chargebee-cli ."""
    result = pyfiglet.figlet_format("chargebee-cli", font="slant")
    click.echo(result)


# cmd 1
@entry_point.group(help='configure the local resources like profile.')
@click.pass_context
def configure(ctx):
    pass


@configure.command("profile", help='configure new profile')
@click.pass_context
@click.option("--name", '-n', type=str, required=True)
@click.option("--api-key", '-ak', type=str, required=True)
@click.option("--account", '-a', type=str, required=True)
def configure_profile_cmd(ctx, name, api_key, account):
    profile_configurator.process(name, {API_KEY_NAME: api_key, ACCOUNT_KEY_NAME: account})


# login command
@entry_point.command("login", help='login to the profile')
@click.pass_context
@click.option("--profile", "-p", required=True, type=str)
def login(ctx, profile):
    login_processor.process(profile)




# add endline at the end
@entry_point.resultcallback()
def process_result(result):
    custom_print("\n.................................end.................................")
    return result


# feedback command
@entry_point.command("feedback", help='provide the feedback')
@click.pass_context
@click.option("--output-format", "-of", default='table', type=str, required=False)
def feedback(ctx, output_format):
    pass


entry_point.add_command(addon_cmd.cmd)
entry_point.add_command(address_cmd.cmd)
entry_point.add_command(card_cmd.cmd)
entry_point.add_command(comment_cmd.cmd)
entry_point.add_command(coupon_cmd.cmd)
entry_point.add_command(coupon_code_cmd.cmd)
entry_point.add_command(coupon_set_cmd.cmd)
entry_point.add_command(credit_note_cmd.cmd)
entry_point.add_command(customer_cmd.cmd)
entry_point.add_command(event_cmd.cmd)

entry_point.add_command(gift_cmd.cmd)
entry_point.add_command(hosted_page_cmd.cmd)
entry_point.add_command(invoice_cmd.cmd)
entry_point.add_command(order_cmd.cmd)
entry_point.add_command(plan_cmd.cmd)
entry_point.add_command(profile_cmd.cmd)
entry_point.add_command(promotional_credit_cmd.cmd)
entry_point.add_command(quote_cmd.cmd)
entry_point.add_command(subscription_cmd.cmd)
entry_point.add_command(transaction_cmd.cmd)
entry_point.add_command(unbilled_charge_cmd.cmd)
entry_point.add_command(theme_cmd.theme_cmd)

