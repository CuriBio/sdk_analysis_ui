"""Setup configuration."""
import os
import sys

from setuptools import Extension
from setuptools import find_packages
from setuptools import setup
from distutils.dir_util import copy_tree

import py2exe
import h5py



base = None

if sys.platform == "win32":
    base = "Win32GUI"

build_exe_options = { 'packages': ['scipy'] }

distDir = 'dist'
h5pyPath = os.path.join( distDir, "h5py")
copy_tree(h5py.__path__[ 0], h5pyPath )

import jsonschema
data_path = os.path.join(os.path.dirname(jsonschema.__loader__.path), 'schemas')
copy_tree(data_path, 'dist/jsonschema/schemas')

includes = ['h5py', 'h5py.defs', 'h5py.utils', 'h5py.h5s', 'h5py.h5p', 'h5py.h5t', 'h5py._conv', 'h5py.h5ac', 'h5py._proxy']
excludes = []

setup(
    windows=["main.py"],
    name="sdk analyzer",
    version="0.2.0",
    description="Tools for analyzing waveforms produced by a Mantarray Instrument",
    url="",
    author="Curi Bio",
    author_email="contact@curibio.com",
    license="MIT",
    install_requires=[
        "pulse3d>=0.20.2",
        "wxPython>=4.1.1",
        "h5py",
        "numpy==1.20.2",
        "scipy==1.6.2",
        "numba>=0.54.1",
        "pandas>=1.3.4",
    ],
    zip_safe=False,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
    ],
    options = {"py2exe": {"compressed": 0,
                          "optimize": 1,
                          "includes": includes,
                          "excludes": excludes,
                          "dist_dir": distDir,
                        }
    }
)

