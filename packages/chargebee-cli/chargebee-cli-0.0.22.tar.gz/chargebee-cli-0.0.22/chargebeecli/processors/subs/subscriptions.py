from chargebeecli.client.actionsImpl import ActionsImpl
from chargebeecli.constants.constants import Formats
from chargebeecli.export.Exporter import Exporter
from chargebeecli.formater.response_formatter import ResponseFormatter
from chargebeecli.printer.printer import Printer, custom_print_table, custom_print
from chargebeecli.processors.customer.subscription_customer import SubscriptionCustomer
from chargebeecli.processors.processor import Processor
from chargebeecli.validator.validator import Validator

API_URI = '/api/v2/subscriptions'


class Subscription(Processor, Validator, ResponseFormatter, Exporter, Printer):
    __action_processor = ActionsImpl()

    def __init__(self, columns_subs, columns_customer, _operation, export_format, export_path, file_name,
                 response_format):
        self.headers = self.get_api_header()
        self.export_format = export_format
        self.export_path = export_path
        self.file_name = file_name
        self.tables = None
        self.response_format = response_format
        self.operation = _operation
        self.export_format = export_format
        self.export_path = export_path
        self.file_name = file_name
        self.tables = None
        self.__columns = columns_subs
        self.headers = self.get_api_header()
        self.__columns_customer = columns_customer
        self.__subscriptionCustomer = SubscriptionCustomer(columns_customer)
        self.headers_customer = self.__subscriptionCustomer.get_api_header()

    def validate_param(self):
        self.headers = super().validate_param(self.__columns, self.headers)
        self.headers_customer = super().validate_param(self.__columns_customer, self.headers_customer)
        return self

    def get_api_header(self):
        return ["activated_at", "auto_collection", "billing_period", "billing_period_unit", "created_at",
                "currency_code", "current_term_end", "current_term_start", "customer_id", "deleted",
                "due_invoices_count", "due_since", "has_scheduled_changes", "id", "mrr", "next_billing_at", "object",
                "plan_amount", "plan_free_quantity", "plan_id", "plan_quantity", "plan_unit_price", "resource_version",
                "started_at", "status", "total_dues", "updated_at"]

    def format(self):
        if self.to_be_formatted():
            self.tables = super(Subscription, self).format(self.response, self.response_format, self.operation,
                                                           self.headers, 'subscription', 'list')
            self.format_customer()
        return self

    def format_customer(self):
        self.tables_customer = super().format(self.response, self.response_format, self.operation,
                                              self.headers_customer, 'customer', 'list')
        return self

    def process(self, ctx, operation, payload, resource_id):
        return super(Subscription, self).process(ctx, operation, payload, resource_id)

    def to_be_formatted(self):
        return self.response_format.lower() == Formats.TABLE.value

    def get(self, ctx, payload, resource_id):
        return self.__action_processor.get(API_URI + '/' + resource_id)

    def list(self, ctx):
        return self.__action_processor.get(API_URI)

    def delete(self, ctx, payload, resource_id):
        return self.__action_processor.delete(API_URI + '/' + resource_id + '/' + 'delete')

    def table_to_be_printed(self):
        return self.to_be_formatted()

    def print_response(self, theme, before=None, after=None):
        if self.table_to_be_printed():
            custom_print_table(self.tables, self.headers, theme)
            custom_print("---------------------------")
            custom_print("........customer.............\n")
            custom_print("           \|/               ")
            custom_print("           /|\               ")
            custom_print_table(self.tables_customer, self.headers_customer, theme)
        else:
            custom_print(self.response.content.decode('utf-8'))
