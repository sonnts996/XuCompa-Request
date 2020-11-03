import json
import logging
import os

from xu.compa.Parapluie.src import PFunction


def getDataFolder():
    path = os.path.join(PFunction.getUserFolder(), "XuCompa")
    if not os.path.isdir(path):
        PFunction.linux_mkdir(PFunction.getUserFolder(), path, "XuCompa")

    p2 = os.path.join(path, "XRequest")
    if not os.path.isdir(p2):
        PFunction.linux_mkdir(path, p2, "XRequest")
    return p2


def getConfigFile():
    return os.path.join(getDataFolder(), "config.json")


def getRequestFolder():
    path = os.path.join(getDataFolder(), "Request")
    if not os.path.isdir(path):
        PFunction.linux_mkdir(getDataFolder(), path, "Request")
    return path, os.path.join(path, "description.xdef")


def getAPILinkFile():
    return os.path.join(getDataFolder(), "api_link.json")


def getConfig():
    if os.path.isfile(getConfigFile()):
        try:
            data = open(getConfigFile(), "r", encoding="utf-8").read()
            obj = json.loads(data)
            return obj
        except Exception as ex:
            logging.exception(ex)
    return {
        "viewer": {
            "last_open": PFunction.getUserFolder()
        },
        "request": {
            "last_open": PFunction.getUserFolder()
        }
    }


def getViewerConfig():
    config = getConfig()

    if "viewer" in config:
        return config["viewer"]
    else:
        config["viewer"] = {
            "last_open": PFunction.getUserFolder()
        }
        return config["viewer"]


def getViewerConfig_LastOpen():
    viewerConfig = getViewerConfig()
    if "last_open" in viewerConfig:
        return viewerConfig["last_open"]
    else:
        viewerConfig["last_open"] = PFunction.getUserFolder()
        return PFunction.getUserFolder()


def getRequestConfig():
    config = getConfig()

    if "request" in config:
        return config["request"]
    else:
        config["request"] = {
            "last_open": PFunction.getUserFolder()
        }
        return config["request"]


def getRequestConfig_LastOpen():
    viewerConfig = getRequestConfig()
    if "last_open" in viewerConfig:
        return viewerConfig["last_open"]
    else:
        viewerConfig["last_open"] = PFunction.getUserFolder()
        return PFunction.getUserFolder()


def updateConfig(config):
    data = json.dumps(config, sort_keys=True, ensure_ascii=False, indent=4)
    f = open(getConfigFile(), "w", encoding="utf-8")
    f.write(data)
    f.close()
