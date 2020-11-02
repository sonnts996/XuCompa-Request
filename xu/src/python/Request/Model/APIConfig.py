import json

from xu.src.python.Request.Model import BodyType
from xu.src.python.Request.Model.APILink import APILink


class APIConfig:

    def __init__(self):
        self.config = {
            "api": "",
            "link": APILink().link,
            "protocol": "",
            "body": "",
            "body_type": "",
            "header": "",
            "param": {},
            "description": ""
        }

    def construct(self, config: dict):
        if 'api' in config:
            self.setAPI(config['api'])
        else:
            self.setAPI("")

        if 'link' in config:
            lnk = APILink()
            lnk.construct(config['link'])
            self.setLink(lnk)
        else:
            self.setLink(APILink())

        if 'param' in config:
            self.setParam(config['param'])
        else:
            self.setParam({})

        if 'protocol' in config:
            self.setProtocol(config['protocol'])
        else:
            self.setProtocol("")

        if 'description' in config:
            self.setDescription(config['description'])
        else:
            self.setDescription("")

        if 'body' in config:
            if 'body_type' in config:
                self.setBody(config['body'], config['body_type'])
            else:
                self.setBody(config['body'], BodyType.Text)
        else:
            self.setBody("", BodyType.Text)

        if 'header' in config:
            self.setHeader(config['header'])
        else:
            self.setHeader({})

    def api(self):
        return self.config['api']

    def link(self):
        return self.config['link']

    def parseLink(self):
        lnk = APILink()
        lnk.construct(self.link())
        return lnk

    def param(self):
        return self.config['param']

    def protocol(self):
        return self.config['protocol']

    def body(self):
        return self.config['body']

    def bodyType(self):
        return self.config['body_type']

    def description(self):
        return self.config['description']

    def header(self):
        return self.config['header']

    def setAPI(self, data: str):
        self.config['api'] = data

    def setLink(self, data: APILink):
        self.config['link'] = data.link

    def setParam(self, data):
        self.config['param'] = data

    def setProtocol(self, data: str):
        self.config['protocol'] = data

    def setBody(self, data, tpe):
        self.config['body'] = data
        self.config['body_type'] = tpe

    def setHeader(self, data):
        self.config['header'] = data

    def setDescription(self, data):
        self.config['description'] = data

    def __str__(self):
        return json.dumps(self.config, ensure_ascii=False, indent=4, sort_keys=False)
