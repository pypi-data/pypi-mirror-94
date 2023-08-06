from chargebeecli.constants.constants import ApiOperation
from chargebeecli.constants.error_messages import OPERATION_NOT_SUPPORTED, ID_IS_NULL
from chargebeecli.printer.printer import custom_print


def _validate_id(_resource_id):
    if _resource_id is None:
        custom_print(ID_IS_NULL, err=True)
        exit()


class Processor(object):

    def get_api_header(self):
        raise NotImplementedError("Please Implement this method")

    def process(self, ctx, operation, payload, resource_id):
        if operation == ApiOperation.CREATE.value:
            self.create(ctx=ctx, payload=payload, resource_id=resource_id)
        elif operation == ApiOperation.FETCH.value:
            _validate_id(resource_id)
            self.response = self.get(ctx=ctx, payload=payload, resource_id=resource_id)
        elif operation == ApiOperation.DELETE.value:
            _validate_id(resource_id)
            self.response = self.delete(ctx=ctx, payload=payload, resource_id=resource_id)
        elif operation == ApiOperation.LIST.value:
            self.response = self.list(ctx=ctx)
        elif operation == ApiOperation.UPDATE.value:
            self.update(ctx=ctx, payload=payload, resource_id=resource_id)
        else:
            custom_print(OPERATION_NOT_SUPPORTED, err=True)
            exit()
        return self

    def get(self, ctx, payload, resource_id):
        raise NotImplementedError("Please Implement this method")

    def list(self, ctx):
        raise NotImplementedError("Please Implement this method")

    def create(self, ctx, payload, resource_id):
        custom_print("feature is not available yet.please contact [ bhasker.nandkishor@gmail.com] .", err=True)
        exit()

    def update(self, ctx, payload, resource_id):
        custom_print("feature is not available yet.please contact [ bhasker.nandkishor@gmail.com] .", err=True)
        exit()

    def delete(self, ctx, payload, resource_id):
        raise NotImplementedError("Please Implement this method")
