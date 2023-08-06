
# create company log
class DtlCompanyLogCreateModel:

    def __init__(self, company_id, log_type): # required fields
        self.company_id = company_id
        self.type = log_type
        self.message = None 

    def get_json_object(self):
        return {
            'companyId': self.company_id,
            'type': self.type,
            'message': self.message,
        }

# update company log
class DtlCompanyLogPatchModel:

    def __init__(self):
        self.company_id = None
        self.type = None
        self.message = None 

    def get_json_object(self):
        return {
            'companyId': self.company_id,
            'type': self.type,
            'message': self.message,
        }