#!/usr/bin/env python3
from setuptools import setup

with open("README.md", "r") as fp:
    long_description = fp.read()

setup(
    name="a38-decimal",
    version="0.1.3",
    description="parse and generate Italian Fattura Elettronica",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Be20",
    author_email="web@be20.it",
    url="https://github.com/gianpieropa/python-a38",
    license="https://www.apache.org/licenses/LICENSE-2.0.html",
    packages=["a38"],
    scripts=["a38tool"],
    install_requires=["python-dateutil", "pytz", "asn1crypto"],
    test_requires=["python-dateutil", "pytz", "asn1crypto"],
    extras_require={
        "formatted_python": ["yapf"],
        "html": ["lxml"],
        "cacerts": ["requests"],
    },
)
