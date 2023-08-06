
# update user
class DtlUserPatchModel:

    def __init__(self):
        self.first_name = None
        self.last_name = None

    def get_json_object(self):
        
        return {
            'firstName': self.first_name,
            'lastName': self.last_name,
        }