import requests

## handles Company API actions
class DtlMessagesController:

    def __init__(self, url):
        self.url = url + "api/messages"

    # NOT IMPLEMENTED


    # def get(self, access_token, message_id = None):
    #     headers = {"Authorization": "Bearer " + access_token}
    #     if(message_id == None):
    #         return requests.get(url = self.url, headers=headers)
    #     else:
    #         url = "{}/{}".format(self.url, message_id)
    #         return requests.get(url = url, headers=headers)

    # def reschedule(self, access_token, json_model):
    #     headers = {"Authorization": "Bearer " + access_token}
    #     return requests.patch(url = self.url, headers=headers, data = json_model)