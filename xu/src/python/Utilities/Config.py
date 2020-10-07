import json
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


def getConfig():
    if os.path.isfile(getConfigFile()):
        try:
            data = open(getConfigFile(), "r", encoding="utf-8").read()
            obj = json.loads(data)
            return obj
        except Exception as ex:
            print(ex)
    return {
        "viewer": {
            "last_open": ""
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


def updateConfig(config):
    data = json.dumps(config, sort_keys=True, ensure_ascii=False, indent=4)
    f = open(getConfigFile(), "w", encoding="utf-8")
    f.write(data)
    f.close()
