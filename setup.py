#!/usr/bin/env python3
from setuptools import setup

with open("README.md") as fp:
    long_description = fp.read()

with open("LICENSE") as fp:
    licence = fp.read()

setup(
    name="argparse_action",
    version="0.1.0",
    description="untility module for argparse to create cli ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=licence,
    maintainer="Nyiro Gergo",
    maintainer_email="gergo.nyiro@gmail.com",
    py_modules=["argparse_action"],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
)
