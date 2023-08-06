
# create campaign
class DtlCampaignCreateModel:

    def __init__(self, company_id, template_id): # required fields
        self.company_id = company_id
        self.template_id = template_id
        self.OnReplyAction = None
        self.ScheduledMailLimit = None

    def get_json_object(self):
        return {
            'companyId': self.company_id,
            'templateId': self.template_id,
            'onReplyAction': self.OnReplyAction,
            'scheduledMailLimit': self.ScheduledMailLimit,
        }

# update campaign
class DtlCampaignPatchModel:

    def __init__(self):
        self.template_id = None
        self.OnReplyAction = None
        self.ScheduledMailLimit = None

    def get_json_object(self):
        return {
            'templateId': self.template_id,
            'onReplyAction': self.OnReplyAction,
            'scheduledMailLimit': self.ScheduledMailLimit,
        }