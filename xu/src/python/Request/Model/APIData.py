"""Example construct:
   {
       "config": {
           "api": "training_comment_getlist",
           "link": {
               "delete": false,
               "id": 3,
               "link": "http://10.96.254.179:5021/api/training/",
               "name": "DAOTAO_BETA"
           },
           "param": {},
           "protocol": "GET",
           "type": "Param"
       },
       "response": {
           "content": [],
           "header": {
               "Content-Type": "application/json; charset=utf-8",
               "Date": "Wed, 22 Jul 2020 09:54:24 GMT",
               "Server": "Kestrel",
               "Transfer-Encoding": "chunked"
           },
           "status": 200,
           "url": "http://10.96.254.179:5021/api/training/training_comment_getlist"
       },
       "save": {
           "description": "",
           "folder": {
               "dir": "C:\\Users\\DEV-C2-2\\HttpRequest\\data",
               "isDir": true,
               "name": "invert"
           },
           "name": "training_comment_getlist.json"
       }
   }"""
from xu.src.python.Request.Model.APIConfig import APIConfig
from xu.src.python.Request.Model.APIResponse import APIResponse


class APIData:

    def __init__(self):
        config = APIConfig().config
        response = APIResponse().response
        self.data = {
            "config": config,
            "response": response
        }

    def construct(self, data: dict):
        if 'config' in data:
            cfg = APIConfig()
            cfg.construct(data['config'])
            self.setConfig(cfg)
        else:
            self.setConfig(APIConfig())

        if 'response' in data:
            cfg = APIResponse()
            cfg.construct(data['response'])
            self.setResponse(cfg)
        else:
            self.setResponse(APIResponse())

    def config(self):
        return self.data['config']

    def parseConfig(self):
        cfg = APIConfig()
        cfg.construct(self.config())
        return cfg

    def response(self):
        return self.data['response']

    def parseResponse(self):
        res = APIResponse()
        res.construct(self.response())
        return res

    def setConfig(self, data: APIConfig):
        self.data['config'] = data.config

    def setResponse(self, data: APIResponse):
        self.data['response'] = data.response
