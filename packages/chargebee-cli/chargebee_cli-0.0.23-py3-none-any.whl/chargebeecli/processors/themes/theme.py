import json

from requests import Response

from chargebeecli.config.Configuration import Configuration
from chargebeecli.constants.constants import ApiOperation, ACTIVE_THEME_SECTION_NAME
from chargebeecli.printer.printer import Printer,  custom_print
from chargebeecli.processors.processor import Processor
from chargebeecli.processors.themes.available_themes import available_themes, get_theme
from chargebeecli.util.printer_util import custom_print_themes
from chargebeecli.validator.validator import Validator


class Theme(Processor, Validator, Printer):

    def __init__(self, export_format, export_path, file_name, response_format, _operation, _input_columns):
        self.export_format = export_format
        self.export_path = export_path
        self.file_name = file_name
        self.tables = None
        self.response_format = response_format
        self.operation = _operation
        self.input_columns = _input_columns

    def process(self, ctx, operation, payload, resource_id):
        return super(Theme, self).process(ctx, operation, payload, resource_id)

    """this is called apply operation"""

    def create(self, ctx, payload, resource_id):
        theme = get_theme(resource_id)
        if theme is None:
            custom_print("Invalid theme: " + resource_id, err=True)
            exit()
        configuration = Configuration.Instance()
        configuration.update_section(ACTIVE_THEME_SECTION_NAME, {'theme': resource_id})
        custom_print(resource_id + " theme is set")
        exit()

    def get(self, ctx, payload, resource_id):
        response = Response()
        response.status_code = 200
        res = []
        for __theme in available_themes:
            if resource_id == __theme['name']:
                res.append({"theme": __theme})
                break

        response._content = json.dumps(res).encode('utf-8')
        return response

    def list(self, ctx):
        response = Response()
        response.status_code = 200
        res = []
        for __theme in available_themes:
            t1 = {"theme": __theme}
            res.append(t1)
        t = {"list": res}
        response._content = json.dumps(t).encode('utf-8')
        return response

    def delete(self, ctx, payload, resource_id):
        custom_print("delete operation is not supported for themes !!", err=True)
        exit()

    def update(self, ctx, payload, resource_id):
        custom_print("update operation is not supported for themes !!", err=True)
        exit()

    def print_response(self, before=None, after=None):
        dict_response = json.loads(self.response.content.decode("utf-8"))
        if self.operation == ApiOperation.FETCH.value:
            res = dict_response
        else:
            res = dict_response["list"]
        custom_print_themes(res)
