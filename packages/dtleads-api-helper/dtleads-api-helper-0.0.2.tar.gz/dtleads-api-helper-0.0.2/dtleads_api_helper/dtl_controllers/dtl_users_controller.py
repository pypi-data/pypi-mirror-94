import requests
import json

## handles account API actions
class DtlUsersController:

    def __init__(self, url):
        self.url = url + "api/users"

    # GET api/users/{id?}
    def get(self, access_token, user_id = None):
        headers = {"Authorization": "Bearer " + access_token}
        if(user_id != None): # user id given
            # get user by Id
            url = "{}/{}".format(self.url, user_id)
            return requests.get(url = url, headers=headers)
        else: 
            # get all users
            return requests.get(url = self.url, headers=headers)

    # PATCH api/users/{id}
    def patch(self, access_token, userId, json_model):
        headers = {"Authorization": "Bearer " + access_token}
        patch_url = "{}/{}".format(self.url, userId)
        return requests.patch(url = patch_url, headers=headers, data = json_model)