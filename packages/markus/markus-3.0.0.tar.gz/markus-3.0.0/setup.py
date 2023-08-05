#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import os
import re
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        import shlex

        # import here, cause outside the eggs aren't loaded
        import pytest

        pytest_args = shlex.split(self.pytest_args) if self.pytest_args else []
        errno = pytest.main(pytest_args)
        sys.exit(errno)


def get_version():
    fn = os.path.join("markus", "__init__.py")
    vsre = r"""^__version__ = ['"]([^'"]*)['"]"""
    version_file = open(fn).read()
    return re.search(vsre, version_file, re.M).group(1)


def get_file(fn):
    with open(fn) as fp:
        return fp.read()


setup(
    name="markus",
    version=get_version(),
    description="Metrics system for generating statistics about your app",
    long_description=(get_file("README.rst") + "\n\n" + get_file("HISTORY.rst")),
    author="Will Kahn-Greene",
    author_email="willkg@mozilla.com",
    url="https://github.com/willkg/markus",
    project_urls={
        "Documentation": "https://markus.readthedocs.io/",
        "Source": "https://github.com/willkg/markus/",
        "Tracker": "https://github.com/willkg/markus/issues",
    },
    extras_require={
        "datadog": ["datadog"],
        "statsd": ["statsd"],
    },
    tests_requires=["pytest"],
    packages=["markus"],
    package_dir={"markus": "markus"},
    cmdclass={"test": PyTest},
    include_package_data=True,
    license="MPLv2",
    zip_safe=False,
    keywords="metrics datadog statsd",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
