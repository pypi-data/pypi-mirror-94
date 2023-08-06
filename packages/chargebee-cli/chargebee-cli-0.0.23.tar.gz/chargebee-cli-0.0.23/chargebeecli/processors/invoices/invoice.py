from chargebeecli.client.actionsImpl import ActionsImpl
from chargebeecli.constants.constants import Formats
from chargebeecli.export.Exporter import Exporter
from chargebeecli.formater.response_formatter import ResponseFormatter
from chargebeecli.printer.printer import Printer
from chargebeecli.processors.processor import Processor
from chargebeecli.validator.validator import Validator

API_URI = '/api/v2/invoices'


class Invoice(Processor, Validator, ResponseFormatter, Exporter, Printer):
    __action_processor = ActionsImpl()

    def __init__(self, export_format, export_path, file_name, response_format, _operation, _input_columns):
        self.headers = self.get_api_header()
        self.export_format = export_format
        self.export_path = export_path
        self.file_name = file_name
        self.tables = None
        self.response_format = response_format
        self.operation = _operation
        self.input_columns = _input_columns

    def validate_param(self):
        self.headers = super().validate_param(self.input_columns, self.headers)
        return self

    def get_api_header(self):
        return ["adjustment_credit_notes", "amount_adjusted", "amount_due", "amount_paid", "amount_to_collect",
                "applied_credits", "base_currency_code", "billing_address", "credits_applied", "currency_code",
                "customer_id", "date", "deleted", "due_date", "dunning_attempts", "exchange_rate", "first_invoice",
                "has_advance_charges", "id", "is_gifted", "issued_credit_notes", "line_items", "linked_orders",
                "linked_payments", "net_term_days", "new_sales_amount", "object", "paid_at", "price_type", "recurring",
                "resource_version", "round_off_amount", "status", "sub_total", "tax", "term_finalized", "total",
                "updated_at", "write_off_amount"]

    def process(self, ctx, operation, payload, resource_id):
        return super(Invoice, self).process(ctx, operation, payload, resource_id)

    def to_be_formatted(self):
        return self.response_format.lower() == Formats.TABLE.value

    def format(self):
        if self.to_be_formatted():
            self.tables = super(Invoice, self).format(self.response, self.response_format, self.operation,
                                                      self.headers, 'invoice', 'list')
        return self

    def get(self, ctx, payload, resource_id):
        return self.__action_processor.get(API_URI + '/' + resource_id)

    def list(self, ctx):
        return self.__action_processor.get(API_URI)

    def delete(self, ctx, payload, resource_id):
        return self.__action_processor.delete(API_URI + '/' + resource_id + '/' + 'delete')

    def table_to_be_printed(self):
        return self.to_be_formatted()
