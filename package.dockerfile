FROM python:3.8.10-slim

WORKDIR /opt/graphgrid-sdk-python

COPY graphgrid_sdk graphgrid_sdk
COPY setup.py setup.py
COPY pyproject.toml pyproject.toml
COPY README.md README.md
COPY scripts/in_container/build-and-upload-package build-and-upload-package
COPY package_requirements.txt package_requirements.txt

RUN pip3 install --upgrade pip && \
    pip3 install -r package_requirements.txt

ENTRYPOINT [ "sh", "build-and-upload-package" ]
CMD []
