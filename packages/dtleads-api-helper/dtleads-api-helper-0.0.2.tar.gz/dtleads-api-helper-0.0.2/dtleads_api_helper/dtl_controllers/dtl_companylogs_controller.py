import requests

## handles Company log API actions
class DtlCompanyLogsController:

    def __init__(self, url):
        self.url = url + "api/companylogs"

    # GET api/companylogs/{id?}
    def get(self, access_token, log_id = None):
        headers = {"Authorization": "Bearer " + access_token}
        if(log_id == None):
            return requests.get(url = self.url, headers=headers)
        else:
            url = "{}/{}".format(self.url, log_id)
            return requests.get(url = url, headers=headers)

    # POST api/companylogs/{id}
    def create(self, access_token, json_model):
        headers = {"Authorization": "Bearer " + access_token}
        return requests.post(url = self.url, headers=headers, data = json_model)

    # PATCH api/companylogs/{id}
    def patch(self, access_token, log_id, json_model):
        headers = {"Authorization": "Bearer " + access_token}
        patch_url = "{}/{}".format(self.url, log_id)
        return requests.patch(url = patch_url, headers=headers, data = json_model)

    # DELETE api/companylogs/{id}
    def delete(self, access_token, log_id):
        headers = {"Authorization": "Bearer " + access_token}
        delete_url = "{}/{}".format(self.url, log_id)
        return requests.delete(url = delete_url, headers=headers)