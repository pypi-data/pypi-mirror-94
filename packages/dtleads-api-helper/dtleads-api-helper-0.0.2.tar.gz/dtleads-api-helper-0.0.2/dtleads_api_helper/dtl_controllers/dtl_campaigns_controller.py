import requests

## handles Campaign API actions
class DtlCampaignsController:

    def __init__(self, url):
        self.url = url + "api/campaigns"

    # GET api/campaigns/{id?}
    def get(self, access_token, campaign_id = None):
        headers = {"Authorization": "Bearer " + access_token}
        if(campaign_id == None):
            return requests.get(url = self.url, headers=headers)
        else:
            url = "{}/{}".format(self.url, campaign_id)
            return requests.get(url = url, headers=headers)

    # POST api/campaigns
    def create(self, access_token, json_model):
        headers = {"Authorization": "Bearer " + access_token}
        return requests.post(url = self.url, headers=headers, data = json_model)

    # PATCH api/campaigns/{id}
    def patch(self, access_token, campaign_id, json_model):
        headers = {"Authorization": "Bearer " + access_token}
        patch_url = "{}/{}".format(self.url, campaign_id)
        return requests.patch(url = patch_url, headers=headers, data = json_model)

    # DELETE api/campaigns/{id}
    def delete(self, access_token, campaign_id):
        headers = {"Authorization": "Bearer " + access_token}
        delete_url = "{}/{}".format(self.url, campaign_id)
        return requests.delete(url = delete_url, headers=headers)

    # PATCH api/campaigns/{id}/turnon
    def turn_on(self, access_token, campaign_id):
        headers = {"Authorization": "Bearer " + access_token}
        delete_url = "{}/{}/turnon".format(self.url, campaign_id)
        return requests.patch(url = delete_url, headers=headers)
    
    # PATCH api/campaigns/{id}/turnoff
    def turn_off(self, access_token, campaign_id):
        headers = {"Authorization": "Bearer " + access_token}
        delete_url = "{}/{}/turnoff".format(self.url, campaign_id)
        return requests.patch(url = delete_url, headers=headers)
