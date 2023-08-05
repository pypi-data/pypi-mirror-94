#!/usr/bin/env python
import datetime

import setuptools

module_info = {
    "name": "mdocument",
    "version": "4.0.{0}".format(int(datetime.datetime.now().timestamp())),
    "description": "Simple DRM for motor client",
    "author": "Yurzs",
    "author_email": "yurzs+mdocument@yurzs.dev",
    "packages": setuptools.find_packages(
        exclude=("tests", "tests.*", "*.tests", "examples")
    ),
    "install_requires": ["motor"],
    "license": "MIT",
    "keywords": ["mongo", "motor", "Document", "ORM"],
    "url": "https://git.yurzs.dev/yurzs/MDocument",
    "classifiers": [
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
}

with open("README.rst") as long_description_file:
    module_info["long_description"] = long_description_file.read()

setuptools.setup(**module_info)
