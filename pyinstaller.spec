#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- mode: python -*-
import inspect
import os
import sys
from stdlib_utils import configure_logging
from stdlib_utils import get_current_file_abs_directory

use_upx = True

configure_logging()
block_cipher = None

# mypy doesn't understand exactly how pyinstaller parses this
sys.modules["FixTk"] = None  # type: ignore
PATH_OF_CURRENT_FILE = os.path.dirname((inspect.stack()[0][1]))

a = Analysis(  # type: ignore # noqa: F821     the 'Analysis' object is special to how pyinstaller reads the file
    ["main.py"],
    pathex=["dist"],
    binaries=[],
    datas=[],
    hiddenimports=[
        'scipy.special.cython_special',
        'flatten_dict',
        #'pulse3D',
        #'pulse3D.plate_recording',
        #'pulse3D.excel_writer',
        #'mantarray_magent_finding',
        #'mantarray_magnet_finding.utils',
        #'mantarray_magnet_finding.magnet_finding',
	#'numba',
        'h5py',
        'h5py.File',
        'h5py.defs',
        'h5py.utils',
        'h5py.h5s',
        'h5py.h5p',
        'h5py.h5t',
        'h5py._conv',
        'h5py.h5ac',
        'h5py._proxy',
        #'pandas',
    ],
    hookspath=[os.path.join(get_current_file_abs_directory(), "hooks")],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

print("Modules/packages found during analysis:")  # allow-print
for this_info in sorted(a.pure, key=lambda x: x[0]):
    print(this_info)  # allow-print


pyz = PYZ(  # type: ignore # noqa: F821   the 'PYZ' object is special to how pyinstaller reads the file
    a.pure, a.zipped_data, cipher=block_cipher
)
exe = EXE(  # type: ignore # noqa: F821   the 'EXE' object is special to how pyinstaller reads the file
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name="pulse3d",
    debug=False,
    strip=False,
    upx=use_upx,
    upx_exclude=[
        "vcruntime140.dll",  # UPX breaks this dll  https://github.com/pyinstaller/pyinstaller/pull/3821
        "qwindows.dll",  # UPX also has trouble with PyQt https://github.com/upx/upx/issues/107
    ],
    runtime_tmpdir=None,
    console=False,
)

