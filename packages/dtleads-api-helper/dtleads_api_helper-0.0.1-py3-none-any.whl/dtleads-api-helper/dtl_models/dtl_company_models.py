
# create company
class DtlCompanyCreateModel:

    def __init__(self, companny_name): # required fields
        self.company_name = companny_name
        self.website = None
        self.industry = None
        self.location = None

    def get_json_object(self):
        return {
            'companyName': self.company_name,
            'website': self.website,
            'industry': self.industry,
            'location': self.location,
        }

# update company
class DtlCompanyPatchModel:

    def __init__(self):
        self.company_name = None
        self.website = None
        self.industry = None
        self.location = None
        self.user_id = None

    def get_json_object(self):
        return {
            'companyName': self.company_name,
            'website': self.website,
            'industry': self.industry,
            'location': self.location,
            'userId': self.user_id
        }