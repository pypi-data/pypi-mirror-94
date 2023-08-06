import dtleads_api_helper.dtl_controllers as dtl_controllers

import requests
import json

## main class to control package methods
class DanielTimothyLeads:

    def __init__(self):
        url = "https://danieltimothyleads.com/" # api hosted url * end with with / *
        self.url = url + "oauth/token" # add endpoint

        ## controllers
        self.account = dtl_controllers.DtlAccountController(url)
        self.users = dtl_controllers.DtlUsersController(url)
        self.subscription = dtl_controllers.DtlSubscriptionController(url)
        self.messages = dtl_controllers.DtlMessagesController(url)

        self.templates = dtl_controllers.DtlTemplatesController(url)
        self.reply_templates = dtl_controllers.DtlReplyTemplatesController(url)
        self.template_settings = dtl_controllers.DtlTemplateSettingsController(url)
        self.setting_restrictions = dtl_controllers.DtlSettingRestrictionsController(url)

        self.companies = dtl_controllers.DtlCompaniesController(url)
        self.company_logs = dtl_controllers.DtlCompanyLogsController(url)
        self.prospects = dtl_controllers.DtlProspectsController(url)
        self.campaigns = dtl_controllers.DtlCampaignsController(url)
        self.campaign_sequences = dtl_controllers.DtlCampaignSequencesController(url)

    ## authorize login to get Oauth Tokens
    def authorize_login(self, userName, password):
        parms = {
            'grant_type': 'password',
            'username': userName,
            'password': password,
        }
        return requests.post(self.url, data = parms)

    ## refresh the access token using the refresh token 
    def refresh_token(self, refresh_token):
        parms = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        }
        return requests.post(self.url, data = parms)

    ## handle requests response (used for testing)
    def handle_response(self, dtl_response):
        status_code = dtl_response.status_code

        data = None
        if(status_code not in [200, 201, 204]):
            try:
                print(dtl_response.json())
            except:
                print(dtl_response)
                print(dtl_response.reason)
                print(dtl_response.request)
                print(dtl_response.status_code)
                print(dtl_response.url)
                print(dtl_response.raw)
        else:
            if(status_code == 204):
                print(status_code)
            else:
                data = dtl_response.json()
        return data