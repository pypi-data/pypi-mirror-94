import requests

## handles Template API actions
class DtlTemplatesController:

    def __init__(self, url):
        self.url = url + "api/templates"

    # GET api/templates/{id?}
    def get(self, access_token, template_id = None):
        headers = {"Authorization": "Bearer " + access_token}
        if(template_id == None):
            return requests.get(url = self.url, headers=headers)
        else:
            url = "{}/{}".format(self.url, template_id)
            return requests.get(url = url, headers=headers)

    # POST api/templates
    def create(self, access_token, json_model):
        headers = {"Authorization": "Bearer " + access_token}
        return requests.post(url = self.url, headers=headers, data = json_model)

    # PATCH api/templates/{id}
    def patch(self, access_token, template_id, json_model):
        headers = {"Authorization": "Bearer " + access_token}
        patch_url = "{}/{}".format(self.url, template_id)
        return requests.patch(url = patch_url, headers=headers, data = json_model)

    # DELETE api/templates/{id}
    def delete(self, access_token, template_id, change_to_template_id):
        headers = {"Authorization": "Bearer " + access_token}
        delete_url = "{}/{}?TemplateIdChange={}".format(self.url, template_id, change_to_template_id)
        return requests.delete(url = delete_url, headers=headers)

    # POST api/templates/{id}/addreply
    def add_reply(self, access_token, template_id, json_model):
        headers = {"Authorization": "Bearer " + access_token}
        add_url = "{}/{}/addreply".format(self.url, template_id)
        return requests.post(url = add_url, headers=headers, data = json_model)

    # DELETE api/templates/{id}/removereply?replyTemplateId={replyTemplateId}
    def remove_reply(self, access_token, template_id, reply_template_id):
        headers = {"Authorization": "Bearer " + access_token}
        delete_url = "{}/{}/removereply?replyTemplateId={}".format(self.url, template_id, reply_template_id)
        return requests.delete(url = delete_url, headers=headers)