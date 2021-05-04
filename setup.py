"""Setup configuration."""
import os
import sys

from setuptools import Extension
from setuptools import find_packages
from setuptools import setup

base = None

if sys.platform == "win32":
    base = "Win32GUI"

build_exe_options = { 'packages': ['scipy'] }

setup(
    name="sdk analyzer",
    version="0.1.0",
    description="Tools for analyzing waveforms produced by a Mantarray Instrument",
    url="",
    author="Curi Bio",
    author_email="contact@curibio.com",
    license="MIT",
    install_requires=[
        "curibio.sdk>=0.14.0",
        "wxPython>=4.1.1",
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
    options = {"build_exe": build_exe_options}
)
