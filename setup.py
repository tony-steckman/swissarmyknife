""" Setup script for the Swiss Army Knife package.
This script uses setuptools to package the utilities for Python developers."""
import pathlib
from setuptools import setup, find_packages


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="swiss-army-knife",
    version="0.0.1",
    description="A collection of useful utilities for Python developers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    find_packages=find_packages(where="src"),
    author="Tony Steckman",
    author_email="tony@tonysteckman.com"

)
