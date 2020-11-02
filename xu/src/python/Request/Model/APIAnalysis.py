class APIAnalysis:
    def __init__(self):
        self.analysis = {
            "URL": "",
            "Status code": "",
            "Status name": "",
            "Total time": "",
            "Content Size": 0,
            "Send Header": ""
        }

    def construct(self, analysis):
        if 'URL' in analysis:
            self.setURL(analysis['URL'])
        else:
            self.setURL("")

        if 'Status code' in analysis:
            self.setStatusCode(analysis['Status code'])
        else:
            self.setStatusCode("")

        if 'Status name' in analysis:
            self.setStatusName(analysis['Status name'])
        else:
            self.setStatusName("")

        if 'Total time' in analysis:
            self.setTotalTime(analysis['Total time'])
        else:
            self.setTotalTime("")

        if 'Send Header' in analysis:
            self.setSendHeader(analysis['Send Header'])
        else:
            self.setSendHeader("")

        if 'Content Size' in analysis:
            self.setContentSize(analysis['Content Size'])
        else:
            self.setContentSize(0)

    def setURL(self, data: str):
        self.analysis['URL'] = data

    def setStatusCode(self, data):
        self.analysis['Status code'] = data

    def setStatusName(self, data):
        self.analysis['Status name'] = data

    def setTotalTime(self, data):
        self.analysis['Total time'] = data

    def setSendHeader(self, data):
        self.analysis['Send Header'] = data

    def setContentSize(self, data):
        self.analysis['Content Size'] = data

    def url(self):
        return self.analysis['URL']

    def statusCode(self):
        return self.analysis['Status code']

    def statusName(self):
        return self.analysis['Status name']

    def totalTime(self):
        return self.analysis['Total time']

    def sendHeader(self):
        return self.analysis['Send Header']

    def contentSize(self):
        return self.analysis['Content Size']
