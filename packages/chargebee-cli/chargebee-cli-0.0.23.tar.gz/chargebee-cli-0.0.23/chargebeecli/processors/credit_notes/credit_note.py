from chargebeecli.client.actionsImpl import ActionsImpl
from chargebeecli.constants.constants import Formats
from chargebeecli.export.Exporter import Exporter
from chargebeecli.formater.response_formatter import ResponseFormatter
from chargebeecli.printer.printer import Printer
from chargebeecli.processors.processor import Processor
from chargebeecli.validator.validator import Validator

API_URI = '/api/v2/credit_notes'


class CreditNote(Processor, Validator, ResponseFormatter, Exporter, Printer):
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
        return ["allocations", "amount_allocated", "amount_available", "amount_refunded", "base_currency_code",
                "create_reason_code", "currency_code", "customer_id", "date", "deleted", "exchange_rate",
                "fractional_correction", "id", "line_item_discounts", "line_item_taxes", "line_items", "linked_refunds",
                "object", "price_type", "reason_code", "reference_invoice_id", "resource_version", "round_off_amount",
                "status", "sub_total", "taxes", "total", "type", "updated_at"]

    def process(self, ctx, operation, payload, resource_id):
        return super(CreditNote, self).process(ctx, operation, payload, resource_id)

    def to_be_formatted(self):
        return self.response_format.lower() == Formats.TABLE.value

    def format(self):
        if self.to_be_formatted():
            self.tables = super(CreditNote, self).format(self.response, self.response_format, self.operation,
                                                         self.headers, 'credit_note', 'list')
        return self

    def get(self, ctx, payload, resource_id):
        return self.__action_processor.get(API_URI + '/' + resource_id)

    def list(self, ctx):
        return self.__action_processor.get(API_URI)

    def delete(self, ctx, payload, resource_id):
        return self.__action_processor.delete(API_URI + '/' + resource_id + '/' + 'delete')

    def table_to_be_printed(self):
        return self.to_be_formatted()
