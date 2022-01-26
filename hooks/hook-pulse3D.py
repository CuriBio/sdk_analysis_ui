# -*- coding: utf-8 -*-
# Based on https://github.com/pyinstaller/pyinstaller/issues/4809
from PyInstaller.utils.hooks import collect_all

datas, binaries, hiddenimports = collect_all("pulse3D")
