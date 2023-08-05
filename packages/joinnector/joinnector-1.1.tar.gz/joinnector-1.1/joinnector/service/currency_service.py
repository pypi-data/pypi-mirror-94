# pylint: disable=useless-super-delegation

from joinnector.service.base_sdk_service import BaseSDKService


class CurrencyService(BaseSDKService):
    def __init__(self, name):
        super().__init__(name)


currency_service = CurrencyService("currency")
