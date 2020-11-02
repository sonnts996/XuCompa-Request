import json
import xml.etree.ElementTree as Et
from xml.dom import minidom

from xu.src.python.Module.ParamEditor import EditorType


def dumps(obj, formatType: EditorType, onError):
    if formatType == EditorType.JSON:
        if isinstance(obj, str):
            return jsonString(obj, onError)
        else:
            return jsonObject(obj)
    elif formatType == EditorType.XML or formatType == EditorType.HTML:
        if isinstance(obj, str):
            return xmlString(obj, onError)
        else:
            return xmlObject(obj, onError)
    else:
        return str(obj)


def jsonObject(obj):
    formatted_json = json.dumps(obj, sort_keys=False, indent=4, ensure_ascii=False)
    return formatted_json


def jsonString(obj, onError):
    try:
        js = json.loads(obj)
        formatted_json = json.dumps(js, sort_keys=False, indent=4, ensure_ascii=False)
        return formatted_json
    except Exception as ex:
        print(ex)
        if onError is not None:
            onError(str(ex))
        return None


def xmlString(xml, onError):
    try:
        if isinstance(xml, bytes):
            xml = xml.decode('utf-8')
        repaired = minidom.parseString(xml)
        return '\n'.join([line for line in repaired.toprettyxml(indent='\t').split('\n') if line.strip()])
    except Exception as ex:
        print(ex)
        if onError is not None:
            onError(str(ex))
        return None


def xmlObject(dom, onError):
    try:
        if isinstance(dom, Et.Element):
            data = Et.tostring(dom, encoding='utf8')
            return xmlString(data, onError)
        else:
            if onError is not None:
                onError("XML Object fail to reading!")
    except Exception as ex:
        print(ex)
        if onError is not None:
            onError(str(ex))
        return None
