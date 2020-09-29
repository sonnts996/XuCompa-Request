import os

from xu.src.res import resources, resource2qrc


def initResource():
    resources.qInitResources()


def runQrc(build=False):
    if build:
        resource2qrc.run(os.path.dirname(resource2qrc.__file__))
    else:
        resource2qrc.runWithoutBuildRes(os.path.dirname(resource2qrc.__file__))
