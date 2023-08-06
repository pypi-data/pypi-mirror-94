#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import find_packages, setup

EXCLUDE_FROM_PACKAGES = ["contrib", "docs", "test*"]
CURDIR = os.path.abspath(os.path.dirname(__file__))

DESCRIPTION = """\
Automagically provides CRUD API to an arbitrary PostgreSQL database"""

def load_requirements(fname):
    try:
        from pip._internal.req import parse_requirements
    except ImportError:
        from pip.req import parse_requirements
    reqs = parse_requirements(fname, session="test")
    try:
        return [str(ir.req) for ir in reqs]
    except:
        return [str(ir.requirement) for ir in reqs]

with open("README.md") as f:
    readme = f.read()

setup(
    name="automapDB",
    description=DESCRIPTION,
    long_description=readme,
    long_description_content_type='text/markdown',
    version="0.0.1rc",
    author="Fabi T.",
    author_email="fabian.thomczyk@uniklinik-freiburg.de",
    url="https://gitlab.com/uklfr/mds/automapDB",
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "automapdb = automapdb.cli:main",
        ]
    },
    zip_safe=False,
    install_requires=load_requirements("requirements.txt"),
    python_requires=">=3.6",
    license="License :: MIT License",
)
