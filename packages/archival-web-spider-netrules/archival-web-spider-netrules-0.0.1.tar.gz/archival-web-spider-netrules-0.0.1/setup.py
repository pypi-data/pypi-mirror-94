#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="archival-web-spider-netrules", # Replace with your own username
    version="0.0.1",
    author="netrules",
    author_email="personal@sgonzalez.tech",
    description="Using BeautifulSoup and Selenium Webdriver to crawl websites and retrieve their resources to keep documentation for educative purposes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/netrules/archival-web-spider",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires='>=3.6',
)
