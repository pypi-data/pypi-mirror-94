import requests

## handles Campaign Sequence API actions
class DtlCampaignSequencesController:

    def __init__(self, url):
        self.url = url + "api/campaignsequences"

    # GET api/campaignsequences/{id?}
    def get(self, access_token, campaign_id = None, prospect_id = None):
        headers = {"Authorization": "Bearer " + access_token}
        if(campaign_id == None or prospect_id == None):
            return requests.get(url = self.url, headers=headers)
        else:
            url = "{}/{}?prospectId={}".format(self.url, campaign_id, prospect_id)
            return requests.get(url = url, headers=headers)

    # POST api/campaignsequences
    def create(self, access_token, json_model):
        headers = {"Authorization": "Bearer " + access_token}
        return requests.post(url = self.url, headers=headers, data = json_model)

    # PATCH api/campaignsequences/{id}
    def patch(self, access_token, companyId, prospect_id, json_model):
        headers = {"Authorization": "Bearer " + access_token}
        patch_url = "{}/{}?prospectId={}".format(self.url, companyId, prospect_id)
        return requests.patch(url = patch_url, headers=headers, data = json_model)

    # DELETE api/campaignsequences/{id}
    def delete(self, access_token, companyId, prospect_id):
        headers = {"Authorization": "Bearer " + access_token}
        delete_url = "{}/{}?prospectId={}".format(self.url, companyId, prospect_id)
        return requests.delete(url = delete_url, headers=headers)