
# update account info
class DtlAccountPatchModel:

    def __init__(self):
        self.company_name = None
        self.phone_number = None

    def get_json_object(self):
        
        return {
            'companyName': self.company_name,
            'phoneNumber': self.phone_number,
        }