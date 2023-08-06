import json

from requests import Response

from chargebeecli.config.Configuration import Configuration
from chargebeecli.constants.constants import Formats, ACTIVE_THEME_SECTION_NAME, ACTIVE_PROFILE_SECTION_NAME, \
    API_KEY_NAME, ACCOUNT_KEY_NAME
from chargebeecli.export.Exporter import Exporter
from chargebeecli.formater.response_formatter import ResponseFormatter
from chargebeecli.printer.printer import Printer
from chargebeecli.processors.processor import Processor
from chargebeecli.validator.validator import Validator


class Profile(Processor, Validator, ResponseFormatter, Exporter, Printer):

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
        return ["name", API_KEY_NAME, ACCOUNT_KEY_NAME]

    def format(self):
        if self.to_be_formatted():
            self.tables = super(Profile, self).format(self.response, self.response_format, self.operation,
                                                      self.headers, 'profile', 'list')
        return self

    def process(self, ctx, operation, payload, resource_id):
        return super(Profile, self).process(ctx, operation, payload, resource_id)

    def get(self, ctx, payload, resource_id):
        response = Response()
        response.status_code = 200
        if resource_id is None:
            __active_profile = Configuration.Instance().fetch_section(ACTIVE_PROFILE_SECTION_NAME, 'primary')
        else:
            __active_profile = resource_id
            if __active_profile not in Configuration.Instance().fetch_available_sections():
                exit()

        if __active_profile is None:
            return response
        res = {"profile": {"name": __active_profile,
                           API_KEY_NAME: Configuration.Instance().fetch_section(__active_profile, API_KEY_NAME),
                           ACCOUNT_KEY_NAME: Configuration.Instance().fetch_section(__active_profile, ACCOUNT_KEY_NAME)}}
        response._content = json.dumps(res).encode('utf-8')
        return response

    def list(self, ctx):
        response = Response()
        response.status_code = 200
        __sections = Configuration.Instance().fetch_available_sections()
        if len(__sections) == 0:
            return response

        res = []
        for __profile in __sections:
            if __profile == ACTIVE_PROFILE_SECTION_NAME or __profile == ACTIVE_THEME_SECTION_NAME:
                continue
            t = {"name": __profile, API_KEY_NAME: Configuration.Instance().fetch_section(__profile, API_KEY_NAME),
                 ACCOUNT_KEY_NAME: Configuration.Instance().fetch_section(__profile, ACCOUNT_KEY_NAME)}
            t1 = {"profile": t}
            res.append(t1)

        t = {"list": res}

        response._content = json.dumps(t).encode('utf-8')
        return response

    def delete(self, ctx, payload, resource_id):
        response = Response()
        response.status_code = 200
        response._content = json.dumps({'profile': {'name': resource_id, 'message': 'deleted'}}).encode('utf-8')
        Configuration.Instance().delete_section_or_profile(resource_id)
        return response

    def table_to_be_printed(self):
        return self.to_be_formatted()

    def to_be_formatted(self):
        return self.response_format.lower() == Formats.TABLE.value
