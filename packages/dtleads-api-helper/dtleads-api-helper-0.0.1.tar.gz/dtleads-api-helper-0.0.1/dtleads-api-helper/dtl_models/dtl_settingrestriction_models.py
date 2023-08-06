
# create setting restrictions
class DtlSettingRestrictionsCreateModel:

    def __init__(self, name): # required fields
        self.name = name

        self.monday = []
        self.tuesday = []
        self.wednesday = []
        self.thursday = []
        self.friday = []
        self.saturday = []
        self.sunday = []

    def get_json_object(self):
        return {
            'restrictionName': self.name,
            'monday': self.monday,
            'tuesday': self.tuesday,
            'wednesday': self.wednesday,
            'thursday': self.thursday,
            'friday': self.friday,
            'saturday': self.saturday,
            'sunday': self.sunday,
        }

# update setting restrictions 
class DtlSettingRestrictionsPatchModel:

    def __init__(self):
        self.name = None

        self.monday = []
        self.tuesday = []
        self.wednesday = []
        self.thursday = []
        self.friday = []
        self.saturday = []
        self.sunday = []

    def get_json_object(self):
        return {
            'restrictionName': self.name,
            'monday': self.monday,
            'tuesday': self.tuesday,
            'wednesday': self.wednesday,
            'thursday': self.thursday,
            'friday': self.friday,
            'saturday': self.saturday,
            'sunday': self.sunday,
        }