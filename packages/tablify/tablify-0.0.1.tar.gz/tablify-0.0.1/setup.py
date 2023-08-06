# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tablify", 
    version="0.0.1",
    author="Kshitij",
    author_email='kshtjkmr35@gmail.com',
    description="This package is used to convert python data structure to html table.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ikshitiz/tablify",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)