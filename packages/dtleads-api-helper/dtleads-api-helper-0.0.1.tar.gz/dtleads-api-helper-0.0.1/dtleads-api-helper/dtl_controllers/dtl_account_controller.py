import requests

## handles account API actions
class DtlAccountController:

    def __init__(self, url):
        self.url = url + "api/account"

    # GET api/account
    def get(self, access_token):
        headers = {"Authorization": "Bearer " + access_token}
        return requests.get(url = self.url, headers=headers)

    # PATCH api/account
    def patch(self, access_token, patch_json_model):
        headers = {"Authorization": "Bearer " + access_token}
        return requests.patch(url = self.url, headers=headers, data = patch_json_model)