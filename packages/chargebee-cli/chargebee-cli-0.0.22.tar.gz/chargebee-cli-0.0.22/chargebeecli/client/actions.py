class Actions(object):

    def get(self, uri, params=None):
        raise NotImplementedError("Please Implement this method")

    def create(self, uri, payload):
        raise NotImplementedError("Please Implement this method")

    def delete(self, uri, payload):
        raise NotImplementedError("Please Implement this method")
