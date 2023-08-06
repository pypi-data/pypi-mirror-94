import http.client


class CreatePayoutAccount:
    def __init__(self, app, key, endpoint) -> None:
        self.app = app
        self.key = key
        self.endpoint = endpoint
        self.route = "/payoutaccount/create"

    def Process(self, request):
        # Create session request
        json_data = json.dumps(request)

        # POST Request for sessionId
        conn = http.client.HTTPSConnection(self.endpoint)
        headers = {'Content-type': 'application/json'}
        # Send the request
        conn.request('POST', self.route, json_data, headers)
        response = json.loads(conn.getresponse().read().decode())

        return response
