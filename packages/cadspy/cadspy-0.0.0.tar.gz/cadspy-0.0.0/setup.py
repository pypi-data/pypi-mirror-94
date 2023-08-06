#!/usr/bin/env python
from setuptools import setup

DISTNAME = "cadspy"
DESCRIPTION = "Stub package"
AUTHOR = "Jake TM Pearce"
AUTHOR_EMAIL = ""
URL = ""
LICENSE = "Copyright 2020"

classifiers = [
    "Development Status :: 7 - Inactive",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "License :: Other/Proprietary License",
    "Intended Audience :: Science/Research",
    "Operating System :: OS Independent",
]

if __name__ == "__main__":
    setup(
        name=DISTNAME,
        version='0.0.0',
        maintainer=AUTHOR,
        maintainer_email=AUTHOR_EMAIL,
        description=DESCRIPTION,
        license=LICENSE,
        url=URL,
        packages=[],
        include_package_data=False,
        zip_safe=True,
        classifiers=classifiers,
        python_requires=">=3.5",
        install_requires=[]
    )
