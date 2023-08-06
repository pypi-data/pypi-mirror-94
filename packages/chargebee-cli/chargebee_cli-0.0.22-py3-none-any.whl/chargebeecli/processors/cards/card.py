from chargebeecli.client.actionsImpl import ActionsImpl
from chargebeecli.constants.constants import Formats
from chargebeecli.export.Exporter import Exporter
from chargebeecli.formater.response_formatter import ResponseFormatter
from chargebeecli.printer.printer import custom_print, Printer
from chargebeecli.processors.processor import Processor
from chargebeecli.validator.validator import Validator

API_URI = '/api/v2/cards'


class Card(Processor, Validator, ResponseFormatter, Exporter, Printer):
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
        return ["card_type", "created_at", "customer_id", "expiry_month", "expiry_year", "funding_type", "gateway",
                "gateway_account_id", "iin", "last4", "masked_number", "object", "payment_source_id",
                "resource_version", "status", "updated_at"]

    def process(self, ctx, operation, payload, resource_id):
        return super(Card, self).process(ctx, operation, payload, resource_id)

    def to_be_formatted(self):
        return self.response_format.lower() == Formats.TABLE.value

    def format(self):
        if self.to_be_formatted():
            self.tables = super(Card, self).format(self.response, self.response_format, self.operation,
                                                   self.headers, 'card', 'list')
        return self

    def get(self, ctx, payload, resource_id):
        return self.__action_processor.get(API_URI + '/' + resource_id)

    def list(self, ctx):
        custom_print('list : operation is not supported for address', err=True)
        exit()

    def delete(self, ctx, payload, resource_id):
        print('delete : operation is not supported for card.')
        exit()
