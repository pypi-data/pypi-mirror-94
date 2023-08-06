import requests

## handles Company API actions
class DtlCompaniesController:

    def __init__(self, url):
        self.url = url + "api/companies"

    # GET api/companies/{id?}
    def get(self, access_token, companyId = None):
        headers = {"Authorization": "Bearer " + access_token}
        if(companyId == None):
            return requests.get(url = self.url, headers=headers)
        else:
            url = "{}/{}".format(self.url, companyId)
            return requests.get(url = url, headers=headers)

    # POST api/companies
    def create(self, access_token, json_model):
        headers = {"Authorization": "Bearer " + access_token}
        return requests.post(url = self.url, headers=headers, data = json_model)

    # PATCH api/companies/{id}
    def patch(self, access_token, companyId, json_model):
        headers = {"Authorization": "Bearer " + access_token}
        patch_url = "{}/{}".format(self.url, companyId)
        return requests.patch(url = patch_url, headers=headers, data = json_model)

    # DELETE api/companies/{id}
    def delete(self, access_token, companyId):
        headers = {"Authorization": "Bearer " + access_token}
        delete_url = "{}/{}".format(self.url, companyId)
        return requests.delete(url = delete_url, headers=headers)