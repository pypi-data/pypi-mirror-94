import requests

## handles Company API actions
class DtlSettingRestrictionsController:

    def __init__(self, url):
        self.url = url + "api/settingrestrictions"

    # GET api/settingrestrictions/{id?}
    def get(self, access_token, restriction_id = None):
        headers = {"Authorization": "Bearer " + access_token}
        if(restriction_id == None):
            return requests.get(url = self.url, headers=headers)
        else:
            url = "{}/{}".format(self.url, restriction_id)
            return requests.get(url = url, headers=headers)

    # POST api/settingrestrictions
    def create(self, access_token, json_model):
        headers = {"Authorization": "Bearer " + access_token}
        return requests.post(url = self.url, headers=headers, data = json_model)

    # PATCH api/settingrestrictions/{id}
    def patch(self, access_token, restriction_id, json_model):
        headers = {"Authorization": "Bearer " + access_token}
        patch_url = "{}/{}".format(self.url, restriction_id)
        return requests.patch(url = patch_url, headers=headers, data = json_model)

    # DELETE api/settingrestrictions/{id}
    def delete(self, access_token, restriction_id):
        headers = {"Authorization": "Bearer " + access_token}
        delete_url = "{}/{}".format(self.url, restriction_id)
        return requests.delete(url = delete_url, headers=headers)