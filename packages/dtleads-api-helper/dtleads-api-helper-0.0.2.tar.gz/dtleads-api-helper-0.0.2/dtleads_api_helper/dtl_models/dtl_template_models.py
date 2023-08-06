
# create template
class DtlTemplateCreateModel:

    def __init__(self, name, subject, html_body): # required fields
        self.name = name
        self.subject = subject
        self.html_body = html_body
        self.template_setting_id = None
        self.unsubscribe_option = None
        
    def get_json_object(self):
        return {
            'name': self.name,
            'subject': self.subject,
            'htmlBody': self.html_body,
            'templateSettingId': self.template_setting_id,
            'unsubscribeOption': self.unsubscribe_option,
        }

# update template
class DtlTemplatePatchModel:

    def __init__(self):
        self.name = None
        self.subject = None
        self.html_body = None
        self.template_setting_id = None
        self.unsubscribe_option = None
        
    def get_json_object(self):
        return {
            'name': self.name,
            'subject': self.subject,
            'htmlBody': self.html_body,
            'templateSettingId': self.template_setting_id,
            'unsubscribeOption': self.unsubscribe_option,
        }

# add reply template
class DtlAddReplyTemplateModel:

    def __init__(self, reply_template_id): # required fields
        self.reply_template_id = reply_template_id
        self.schedule_time = None # default template settings time if null

    def get_json_object(self):
        return {
            'replyTemplateId': self.reply_template_id,
            'scheduleTime': self.schedule_time,
        }