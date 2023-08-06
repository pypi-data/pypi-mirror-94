import requests

## handles Template API actions
class DtlReplyTemplatesController:

    def __init__(self, url):
        self.url = url + "api/replytemplates"

    # GET api/replytemplates/{id?}
    def get(self, access_token, reply_template_id = None):
        headers = {"Authorization": "Bearer " + access_token}
        if(reply_template_id == None):
            return requests.get(url = self.url, headers=headers)
        else:
            url = "{}/{}".format(self.url, reply_template_id)
            return requests.get(url = url, headers=headers)

    # POST api/replytemplates
    def create(self, access_token, json_model):
        headers = {"Authorization": "Bearer " + access_token}
        return requests.post(url = self.url, headers=headers, data = json_model)

    # PATCH api/replytemplates/{id}
    def patch(self, access_token, reply_template_id, json_model):
        headers = {"Authorization": "Bearer " + access_token}
        patch_url = "{}/{}".format(self.url, reply_template_id)
        return requests.patch(url = patch_url, headers=headers, data = json_model)

    # DELETE api/replytemplates/{id}
    def delete(self, access_token, reply_template_id):
        headers = {"Authorization": "Bearer " + access_token}
        delete_url = "{}/{}".format(self.url, reply_template_id)
        return requests.delete(url = delete_url, headers=headers)