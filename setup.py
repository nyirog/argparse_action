#!/usr/bin/env python3
from setuptools import setup

with open("README.md") as fp:
    long_description = fp.read()

setup(
    name="argparse_action",
    version="0.3.1",
    description="confgiure argparse from function signature",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache 2",
    maintainer="Nyiro Gergo",
    maintainer_email="gergo@nyiro.name",
    packages=["argparse_action"],
    python_requires='>=3.6',
    url="https://github.com/nyirog/argparse_action",
    project_urls={
        "Documentation": "https://argparse-action.readthedocs.io/en/latest/",
        "Source": "https://github.com/nyirog/argparse_action",
        "Tracker": "https://github.com/nyirog/argparse_action/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
)
