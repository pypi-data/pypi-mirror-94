
# create reply template
class DtlReplyTemplateCreateModel:

    def __init__(self, name, html_body): # required fields
        self.name = name
        self.html_body = html_body

    def get_json_object(self):
        return {
            "name": self.name,
            "htmlBody": self.html_body,
        }

# update reply template
class DtlReplyTemplatePatchModel:

    def __init__(self):
        self.name = None
        self.html_body = None

    def get_json_object(self):
        return {
            "name": self.name,
            "htmlBody": self.html_body,
        }