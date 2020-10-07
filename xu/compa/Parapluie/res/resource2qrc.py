import os
import xml.etree.ElementTree as XML


def convert(src_folder: str, dest_file: str, filters: list):
    rs = []
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            filename, file_extension = os.path.splitext(file)
            if file_extension in filters:
                path = os.path.join(root, file).replace(src_folder + os.sep, "")
                rs.append(path)
                print(path)
    tree = toQRC(rs)
    tree.write(dest_file)
    export2Define(rs)
    print("")
    print("Use to build resource: pyrcc5 -o resources.py resources.qrc")
    print("Use to build resource: rcc -binary resources.qrc -o resources.rcc")


def toQRC(lst: list):
    xml = XML.Element("RCC")
    tree = XML.ElementTree(xml)
    for file in lst:
        elem = file.split(os.sep)
        prefix = "_".join(elem[:len(elem) - 1])
        if len(elem) > 1:
            final = None
            for subelem in xml.findall("qresource"):
                if subelem.get("prefix") == prefix:
                    final = subelem
                    break
            if final is not None:
                data = XML.SubElement(final, "file")
                data.set("alias", os.path.basename(file))
                data.text = file
            else:
                final = XML.SubElement(xml, "qresource")
                final.set("prefix", prefix)
                data = XML.SubElement(final, "file")
                data.set("alias", os.path.basename(file))
                data.text = file
        else:
            final = XML.SubElement(xml, "qresource")
            data = XML.SubElement(final, "file")
            data.set("alias", os.path.basename(file))
            data.text = file
    return tree


def run(runDir: str = None):
    runWithoutBuildRes(runDir)
    print("")
    print("run", "pyrcc5 -o resources.py resources.qrc", sep=": ")
    print("")
    code = os.system("pyrcc5 -o resources.py resources.qrc")
    print("resource build done!!!", "\ncode: ", code)


def export2Define(lst: list):
    print("")
    print("Icon define")
    fin = []
    for item in lst:
        file = FileDefine(item)
        if file not in fin:
            fin.append(file)

    for item in fin:
        print("Icon_", item.name, ": Final[str] = \"", item.path, "\"", sep="")
    print("")


class FileDefine:
    def __init__(self, path):
        self.name = os.path.basename(path).replace(".", "_").replace("-", "_").title()
        self.path =  os.path.basename(path)

    def __eq__(self, other):
        if isinstance(other, FileDefine):
            other.__class__ = FileDefine
            return self.name == other.name and self.path == other.path
        else:
            return False


def runWithoutBuildRes(runDir: str = None):
    import os
    if runDir is not None:
        os.chdir(runDir)
    convert("../res", "resources.qrc", [".svg", ".css", ".png"])


if __name__ == '__main__':
    run()
