import os
from pathlib import Path

import pandas as pd

from chargebeecli.constants.constants import Export_Formats, Export_Formats_Extensions, ERROR_HEADER, Formats
from chargebeecli.printer.printer import custom_print

_DEFAULT_OUTPUT_FILE_NAME = 'result'

_DEFAULT_EXCEL_SHEET_NAME = 'sheet'


def _get_compression_options(__compression, __file_name=_DEFAULT_OUTPUT_FILE_NAME):
    if __compression:
        return dict(method='zip', archive_name=__file_name)
    return None


def _is_format_accepted(export_format):
    if export_format in list(map(str, Export_Formats.value)):
        return True
    return False


class Exporter(object):

    def __init__(self, headers, data):
        self.headers = headers
        self.data = data
        self.df = pd.DataFrame(self.data, columns=self.headers)

    def to_be_exported(self):
        return self.export_format and self.export_path and self.file_name and \
               self.response_format.lower() == Formats.TABLE.value

    def export_data(self):
        if self.response.status_code != 200:
            self.headers = ERROR_HEADER
        if self.to_be_exported():
            Exporter(self.headers, self.tables).export(_path=self.export_path, _export_format=self.export_format,
                                                       _file_name=self.file_name)
        return self

    def export(self, _path, _export_format, _file_name=_DEFAULT_OUTPUT_FILE_NAME, compression=False):
        try:
            if Export_Formats.CSV.value.lower() == _export_format.lower():
                self.export_csv(path=_path, _file_name=_file_name, compression=_get_compression_options(compression))
            elif Export_Formats.EXCEL.value.lower() == _export_format.lower():
                self.export_excel(path=_path, _file_name=_file_name)
            elif Export_Formats.HTML.value.lower() == _export_format.lower():
                self.export_html(path=_path, _file_name=_file_name)
            else:
                custom_print('format not supported', err=True)
                exit()

            custom_print('!!!  exported !!')
        except Exception as e:
            custom_print(e, err=True)

    def export_csv(self, path, _file_name, compression):
        self.df.to_csv(Path(os.path.join(path, _file_name + Export_Formats_Extensions.CSV.value)),
                       compression=compression, index=False)

    def export_excel(self, _file_name, path):
        self.df.to_excel(os.path.join(path, _file_name + Export_Formats_Extensions.EXCEL.value),
                         sheet_name=_DEFAULT_EXCEL_SHEET_NAME,
                         index=False)

    def export_html(self, _file_name, path):
        self.df.to_html(Path(os.path.join(path, _file_name + Export_Formats_Extensions.HTML.value)),
                        classes='table-striped', index=False)
