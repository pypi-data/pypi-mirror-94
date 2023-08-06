import http.client
import json


class CreatePayoutAccount:
    def __init__(self, app, key, endpoint) -> None:
        self.app = app
        self.key = key
        self.endpoint = endpoint
        self.route = "/payoutaccount/create"

    def Process(self, request):
        # Create request
        json_data = json.dumps(request)
        conn = http.client.HTTPSConnection(self.endpoint)
        headers = {"Content-type": "application/json",
                   "Accept": "application/json"}
        try:
            # Send the request
            conn.request('POST', self.route, json_data, headers)
            response = conn.getresponse()
            if response.status == 200:
                return json.loads(response.read().decode())
            else:
                return {
                    "code": response.status,
                    "error": response.reason
                }
        finally:
            conn.close()
