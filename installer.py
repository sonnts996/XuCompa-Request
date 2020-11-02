import os

import PyInstaller.__main__

request = [
    # '--noconfirm',
    '--clean',
    '--name=XuCompa - Request',
    # '--onefile',
    '--noconsole',
    '--windowed',
    '--icon=' + os.path.join("", 'xu\\src\\res\\window_icon\\link_256px.ico'),
    os.path.join("", 'xu\\src\\python\\main.py'),
]

PyInstaller.__main__.run(request)
