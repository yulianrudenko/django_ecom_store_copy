import sys

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "AXOE_xVY3cNceZ06BjwkpmYR9kxZkYCpDxdwyPyV1yqfrsESI5oso7X0l4KCvN300vUCoipAKhC_97bS"
        self.client_secret = "EFkCv9V5wdhHAlaq0zrUSssL8I-4EHejuQa2w11oqLVlhCwIF2xqi5FFUDMznnJMfTkTahUiWE3-_PoG"
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)
