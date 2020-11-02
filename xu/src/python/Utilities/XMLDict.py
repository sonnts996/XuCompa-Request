test = """<DocumentElement attr="10">
            <Data>
                <DocEntry text="ha">322</DocEntry>
                <LineNum>3</LineNum>
                <U_status>1</U_status>
            </Data>
            <Test>
                <DocEntry>322</DocEntry>
                <LineNum>4</LineNum>
                <U_status>0</U_status>
            </Test>
            <Data>
                <DocEntry text="ab">test q</DocEntry>
                <LineNum>3</LineNum>
                <U_status>1</U_status>
            </Data>
            <Data>
                <DocEntry text="be" value="0">qind</DocEntry>
                <LineNum>3</LineNum>
                <U_status>nomnom</U_status>
            </Data>
        </DocumentElement>"""

import xml.etree.ElementTree as Et


def testData():
    xmlDict = XMLDict()
    xmlDict.xmlString2dict(test)


class XMLDict:
    def __init__(self):
        self.dataDict: dict = {}
        self.xmlObject: Et.Element = Et.Element("")

    def xmlString2dict(self, xml: str):
        dom = Et.fromstring(xml)

        self.dataDict = {dom.tag: []}
        if dom.attrib != {}:
            self.dataDict['attr'] = dom.attrib
        self.getDeep(dom, self.dataDict[dom.tag])
        print(self.dataDict)

    def getDeep(self, xmlObject: Et.Element, root: list):
        for elem in xmlObject:
            text: str = elem.text
            if not text.isspace() and text != "":
                new = {elem.tag: elem.text}
                if elem.attrib != {}:
                    new['attr'] = elem.attrib
                root.append(new)
                self.getDeep(elem, root)
            else:
                new = {elem.tag: []}
                if elem.attrib != {}:
                    new['attr'] = elem.attrib
                root.append(new)
                self.getDeep(elem, new[elem.tag])

    def dict2xmlString(self, dic: dict):
        pass


if __name__ == '__main__':
    testData()
