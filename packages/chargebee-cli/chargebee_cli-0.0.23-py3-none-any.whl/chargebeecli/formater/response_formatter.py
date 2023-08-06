import json

from chargebeecli.constants.constants import Formats, ERROR_HEADER


def _create_table(__response, __format, __operation, __headers, __resource_type, __list_key):
    table = []
    tables = []
    if __operation == __list_key:
        resources = json.loads(__response.content.decode('utf-8'))[__list_key]
        for __resource in resources:
            __resource = __resource[__resource_type]
            table = []
            for header in __headers:
                s = __resource.get(header, None)
                table.append(s)
            tables.append(table)
    else:
        if __resource_type is None:
            data = json.loads(__response.content.decode('utf-8'))
        else:
            data = json.loads(__response.content.decode('utf-8'))[__resource_type]
        for header in __headers:
            table.append(data.get(header, None))
        tables.append(table)

    # custom_print(tabulate(tables, __headers, tablefmt="grid", stralign="center", showindex=True))
    return tables


class ResponseFormatter:

    def to_be_formatted(self):
        raise NotImplementedError("Please Implement this method")

    def format(self):
        raise NotImplementedError("Please Implement this method")

    def format(self, __response, __format, __operation, __headers, __resource_type, __list_key='list'):
        if __response.status_code != 200:
            if __format.lower() != Formats.JSON.value.lower():
                return _create_table(__response, __format, __operation, ERROR_HEADER, None, None)
            # custom_print(__response.content.decode('utf-8'), err=True)
            return self
        if __format.lower() == Formats.JSON.value.lower():
            # custom_print(__response.content)
            return self

        return _create_table(__response, __format, __operation, __headers, __resource_type, __list_key)
