import json

import click
from tabulate import tabulate

from chargebeecli.client.actionsImpl import ActionsImpl
from chargebeecli.constants.constants import Formats
from chargebeecli.processors.customer.customer import Customer


class SubscriptionCustomer(Customer):
    __action_processor = ActionsImpl()

    def __init__(self, columns_customer):
        self.__columns_customer = columns_customer

    def get_api_header(self):
        return ["id", "first_name", "email", "auto_collection", "net_term_days", "allow_direct_debit", "created_at",
                "taxability", "updated_at", "pii_cleared", "resource_version", "deleted", "object", "card_status",
                "promotional_credits", "refundable_credits", "excess_payments", "unbilled_charges",
                "preferred_currency_code", "primary_payment_source_id", "payment_method"]

    def format(self, __format, __operation):
        if self.response.status_code != 200:
            return self

        if __format == Formats.JSON.value:
            click.echo(self.response.content)
            return self

        table = []
        tables = []
        if __operation == 'list':
            plans = json.loads(self.response.content.decode('utf-8'))['list']
            for __plan in plans:
                __plan = __plan['plan']
                table = []
                for header in self.headers:
                    p = __plan.get(header, None)
                    table.append(p)
                tables.append(table)
        else:
            data = json.loads(self.response.content.decode('utf-8'))['plan']
            for header in self.headers:
                table.append(data.get(header, None))
            tables.append(table)

        click.echo(tabulate(tables, self.headers, tablefmt="grid", stralign="center", showindex=True))
        return self

    def process(self, ctx, operation, payload, resource_id):
        return super(SubscriptionCustomer, self).process(ctx, operation, payload, resource_id)
