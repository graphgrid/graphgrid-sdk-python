import os
from pathlib import Path
from setuptools import setup, find_packages

PACKAGE_NAME = "graphgrid-sdk"

top_level_path = Path(__file__).parent.absolute()
with open(os.path.join(top_level_path, "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name=PACKAGE_NAME,
    version="2.0.0a1",
    packages=find_packages(),
    url="https://docs.graphgrid.com/2.0/#/",
    license="",
    author="graphgrid",
    author_email="",
    description="GraphGrid Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=[
        "requests~=2.27.1",
    ],
    python_requires="!=3.9.*, >=3.6",
)
