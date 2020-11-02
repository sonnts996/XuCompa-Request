class APILink:

    def __init__(self):
        self.link = {
            "url": "",
            "name": ""
        }

    def construct(self, link: dict):
        if 'url' in link:
            self.setURL(link['url'])
        else:
            self.setURL("")

        if 'name' in link:
            self.setName(link['name'])
        else:
            self.setName("")

    def url(self):
        if self.link['url'].endswith("/"):
            return self.link['url']
        else:
            return self.link['url'] + "/"

    def name(self):
        return self.link['name']

    def setURL(self, data: str):
        self.link['url'] = data

    def setName(self, data: str):
        self.link['name'] = data
