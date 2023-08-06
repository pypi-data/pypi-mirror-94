"""
Script for creating a package to upload to PYPI
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="password-generator-pkg-Nocturnal-Devil",
    version="0.1.1",
    author="Devil-Shinji",
    author_email="frank.m.kiibus@gmail.com",
    description="Password hasher",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Devil-Shinji/Password-Generator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
