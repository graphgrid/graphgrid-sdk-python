import os
from pathlib import Path
from setuptools import setup, find_packages

PACKAGE_NAME = "gg_sdk"

top_level_path = Path(__file__).parent.absolute()
with open(os.path.join(top_level_path, "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name=PACKAGE_NAME,
    version="0.0.1",
    packages=find_packages(),
    url="",
    license="",
    author="graphgrid",
    author_email="",
    description="GG CORE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=[
    ],
    python_requires="!=3.9.*, >=3.6",
)
