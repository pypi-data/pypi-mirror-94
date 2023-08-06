import base64
import urllib

import requests

from chargebeecli.client.actions import Actions
from chargebeecli.config.Configuration import Configuration
from chargebeecli.constants.constants import API_KEY_NAME, ACCOUNT_KEY_NAME
from chargebeecli.constants.error_messages import UNABLE_TO_CONNECT_OR_TIMED_OUT
from chargebeecli.printer.printer import custom_print


def _auth_header():
    config_data = Configuration.Instance().get_account_api_key()
    b64_val = base64.b64encode(('%s:' % config_data[API_KEY_NAME]).encode('latin1')).strip().decode('latin1')
    return {API_KEY_NAME: {"Authorization": "Basic %s" % b64_val}, ACCOUNT_KEY_NAME: config_data[ACCOUNT_KEY_NAME]}


def build_url(base_url, path, args_dict):
    url_parts = list(urllib.parse.urlparse(base_url))
    url_parts[2] = path
    url_parts[4] = urllib.parse.urlencode(args_dict)
    return urllib.parse.urlunparse(url_parts)


class ActionsImpl(Actions):

    def get(self, uri, params={}):
        config_info = _auth_header()
        r = None
        try:
            url = build_url(config_info[ACCOUNT_KEY_NAME], uri, params)
            r = requests.get(url, params, headers=config_info[API_KEY_NAME])
        except requests.exceptions.RequestException as e:
            custom_print(UNABLE_TO_CONNECT_OR_TIMED_OUT, err=True)
            exit()
        return r

    def create(self, uri, payload):
        config_info = _auth_header()
        r = None
        try:
            url = build_url(config_info[ACCOUNT_KEY_NAME], uri, {})
            r = requests.post(url, data=payload, headers=config_info[API_KEY_NAME])
        except requests.exceptions.RequestException as e:
            custom_print(UNABLE_TO_CONNECT_OR_TIMED_OUT, err=True)
            exit()
        return r

    def delete(self, uri, payload=None):
        return self.create(uri, payload)
