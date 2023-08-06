
# create campaign sequence
class DtlCampaignSequenceCreateModel:

    def __init__(self, campaign_id, prospect_id): # required fields
        self.campaign_id = campaign_id
        self.prospect_id = prospect_id
        self.index_order = None

    def get_json_object(self):
        return {
            "campaignId": self.campaign_id,
            "prospectId": self.prospect_id,
            "indexOrder": self.index_order,
        }

# update campaign sequence
class DtlCampaignSequencePatchModel:

    def __init__(self):
        self.index_order = None

    def get_json_object(self):
        return {
            "indexOrder": self.index_order,
        }