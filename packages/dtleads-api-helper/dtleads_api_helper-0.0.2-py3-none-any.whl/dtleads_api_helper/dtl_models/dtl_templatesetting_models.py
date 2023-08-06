
# create template settings
class DtlTemplateSettingsCreateModel:

    def __init__(self, setting_name, time_in_minutes): # required fields
        self.setting_name = setting_name
        self.schedule_time = time_in_minutes
        self.restriction_id = None

    def get_json_object(self):
        return {
            'settingName': self.setting_name,
            'scheduleTime': self.schedule_time,
            'restrictionId': self.restriction_id
        }

# update template settings
class DtlTemplateSettingsPatchModel:

    def __init__(self):
        self.setting_name = None
        self.schedule_time = None
        self.restriction_id = None


    def get_json_object(self):
        return {
            'settingName': self.setting_name,
            'scheduleTime': self.schedule_time,
            'restrictionId': self.restriction_id
        }