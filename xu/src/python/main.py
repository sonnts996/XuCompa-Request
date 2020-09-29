import sys

import xu.src.python.Window as XWin


def main():
    code = XWin.Application.app(sys.argv)
    sys.exit(code)


if __name__ == '__main__':
    main()
