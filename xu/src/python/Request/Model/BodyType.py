from typing import Final

Text: Final[str] = "application/text; charset=utf-8"
JSON: Final[str] = "application/json; charset=utf-8"
XML: Final[str] = "application/xml; charset=utf-8"
Javascript: Final[str] = "application/javascript; charset=utf-8"
HTML: Final[str] = "application/html; charset=utf-8"


def get(contentType: str):
    return contentType.replace(" ", "").split(";")


def getContentType(contentType: str):
    data = get(contentType)
    if len(data) > 1:
        charset = data[1].replace("charset=", "")
    else:
        charset = None
    return data[0], charset
