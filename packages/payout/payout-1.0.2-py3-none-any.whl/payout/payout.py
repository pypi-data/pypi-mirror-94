import http.client

from payout.create_payout_account import CreatePayoutAccount


class Payout:
    def __init__(self, app, key) -> None:
        self.app = app
        self.key = key
        # Get app endpoints
        conn = http.client.HTTPSConnection("dashboard.redshepherd.com")
        route = "/app/endpoints/" + self.app
        # Send the request
        conn.request('POST', route)
        response = json.loads(conn.getresponse().read().decode())
        # Parse and set dataEndpoints
        if "dataEndpoints" in response:
            self.dataEndpoints = response["dataEndpoints"]
        else:
            self.dataEndpoints = "ERROR Unable to get dataEndpoints from server"
        print("dataEndpoints -> " + self.dataEndpoints)

        # Parse and set redpayEndpoints
        if "redpayEndpoints" in response:
            self.redpayEndpoints = response["redpayEndpoints"]
        else:
            self.redpayEndpoints = "ERROR Unable to get redpayEndpoints from server"
        print("redpayEndpoints -> " + self.redpayEndpoints)

    def CreatePayoutAccount(self, request):
        create_payout_account = CreatePayoutAccount(
            self.app, self.dataEndpoints)
        return create_payout_account.Process(request)

    def UpdatePayoutAccount(self, request):
        pass

    def AddPaymentRate(self, request):
        pass

    def AddPaymentToken(self, request):
        pass
