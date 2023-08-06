# Author: yuce
# Created on: 2021-02-09, at: 15:04 +0300

import sys
import os
import io
import os.path
from setuptools import setup

with io.open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(name="hazelcast",
      version="0.1.0",
      url="",
      download_url="",
      author="Hazecast Engineering",
      author_email="",
      description="",
      long_description=long_description,
      long_description_content_type="text/markdown",
      license="",
      packages=["hazelcast"],
      keywords=["hazelcast"],
      tests_require=[],
      classifiers=[],
)
