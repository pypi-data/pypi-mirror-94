import requests

## handles account API actions
class DtlSubscriptionController:

    def __init__(self, url):
        self.url = url + "api/subscription"

    # GET api/subscription
    def get(self, access_token):
        headers = {"Authorization": "Bearer " + access_token}
        return requests.get(url = self.url, headers=headers)