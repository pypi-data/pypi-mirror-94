import requests

## handles Company API actions
class DtlTemplateSettingsController:

    def __init__(self, url):
        self.url = url + "api/templatesettings"

    # GET api/templatesettings/{id?}
    def get(self, access_token, setting_id = None):
        headers = {"Authorization": "Bearer " + access_token}
        if(setting_id == None):
            return requests.get(url = self.url, headers=headers)
        else:
            url = "{}/{}".format(self.url, setting_id)
            return requests.get(url = url, headers=headers)

    # POST api/templatesettings
    def create(self, access_token, json_model):
        headers = {"Authorization": "Bearer " + access_token}
        return requests.post(url = self.url, headers=headers, data = json_model)

    # PATCH api/templatesettings/{id}
    def patch(self, access_token, setting_id, json_model):
        headers = {"Authorization": "Bearer " + access_token}
        patch_url = "{}/{}".format(self.url, setting_id)
        return requests.patch(url = patch_url, headers=headers, data = json_model)

    # DELETE api/templatesettings/{id}
    def delete(self, access_token, setting_id):
        headers = {"Authorization": "Bearer " + access_token}
        delete_url = "{}/{}".format(self.url, setting_id)
        return requests.delete(url = delete_url, headers=headers)