# (C) Copyright IBM Corp. 2021.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from setuptools import setup, find_packages

NAME = "srikanth-test-python-sdk"
VERSION = "1.0.1"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "python-dateutil>=2.8",
    "requests>=2.20,<3.0",
    "websocket-client==0.48.0"
]
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name=NAME,
    version=VERSION,
    author="ME",
    author_email="kms100@gmail.com",
    description="Python server SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache 2.0",
    url="https://github.com/IBM/appconfiguration-python-sdk",
    packages=find_packages(),
    install_requires=REQUIRES,
    include_package_data=True,
    keywords=['python', 'ibm_appconfiguration'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'License :: OSI Approved :: Apache Software License',
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.0'
)
