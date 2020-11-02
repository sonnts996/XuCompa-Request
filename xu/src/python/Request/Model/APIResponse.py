from xu.src.python.Request.Model.APIAnalysis import APIAnalysis


class APIResponse:

    def __init__(self):
        self.response = {
            "content": "",
            "header": {},
            "status": 0,
            'analysis': APIAnalysis().analysis
        }

    def construct(self, response: dict):
        if 'content' in response:
            self.setContent(response['content'])
        else:
            self.setContent({})

        if 'header' in response:
            self.setHeader(response['header'])
        else:
            self.setHeader({})

        if 'status' in response:
            self.setStatus(response['status'])
        else:
            self.setStatus(0)

        if 'analysis' in response:
            a = APIAnalysis()
            a.construct(response['analysis'])
            self.setAnalysis(a)
        else:
            self.setAnalysis(APIAnalysis())

    def content(self):
        return self.response['content']

    def header(self):
        return self.response['header']

    def status(self):
        return self.response['status']

    def analysis(self):
        return self.response['analysis']

    def setContent(self, data):
        self.response['content'] = data

    def setHeader(self, data):
        self.response['header'] = data

    def setStatus(self, data: int):
        self.response['status'] = data

    def setAnalysis(self, data: APIAnalysis):
        self.response['analysis'] = data.analysis

    def parseAnalysis(self):
        a = APIAnalysis()
        a.construct(self.analysis())
        return a
