#!/usr/bin/env python

import codecs
import os

from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="pirates",
    version="0.5.0",
    license="MIT",
    description="Django app for users, teamds and groups.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Jan Bednařík",
    author_email="jan.bednarik@gmail.com",
    url="https://gitlab.pirati.cz/to/pirates",
    packages=["pirates"],
    include_package_data=True,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Topic :: Utilities",
    ],
    project_urls={
        # "Documentation": "https://pirates.readthedocs.io/",
        # "Changelog": "https://pirates.readthedocs.io/en/latest/changelog.html",
        "Issue Tracker": "https://gitlab.pirati.cz/to/pirates/issues",
    },
    keywords=["django", "openid", "sso"],
    python_requires=">=3.6",
    install_requires=["mozilla-django-oidc>=1.2.4,<2"],
)
