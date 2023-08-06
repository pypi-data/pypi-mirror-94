from chargebeecli.util.printer_util import custom_print_table, custom_print


class Printer(object):

    def table_to_be_printed(self):
        raise NotImplementedError("Please Implement this method")

    def print_response(self, theme, before=None, after=None):
        if self.table_to_be_printed():
            custom_print_table(self.tables, self.headers, theme=theme)
        else:
            custom_print(self.response.content.decode('utf-8'))
