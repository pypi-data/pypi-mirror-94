
# create prospect
class DtlProspectCreateModel:

    def __init__(self, company_id): # required fields
        self.first_name = None
        self.last_name = None
        self.email = None
        self.title = None
        self.company_id = company_id

    def get_json_object(self):
        return {
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "title": self.title,
            "companyId": self.company_id
        }

# update prospect
class DtlProspectPatchModel:

    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.email = None
        self.title = None
        self.company_id = None

    def get_json_object(self):
        return {
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "title": self.title,
            "companyId": self.company_id
        }