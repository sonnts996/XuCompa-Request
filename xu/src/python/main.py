import logging
import os
import sys

import xu.src.python.Window as XWin
from xu.src.python.Utilities import Config


def main():
    logging.basicConfig(filename=os.path.join(Config.getDataFolder(), "request.log"),
                        level=logging.INFO,
                        datefmt="%m/%d/%Y %H:%M:%S")
    code = XWin.Application.app(sys.argv)
    sys.exit(code)


if __name__ == '__main__':
    main()
