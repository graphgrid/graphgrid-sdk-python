FROM python:3.9-slim

WORKDIR /opt/graphgrid-sdk-python

COPY ggcore ggcore
COPY ggsdk ggsdk
COPY tests tests
COPY .coveragerc .coveragerc
COPY .pylintrc .pylintrc
COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]
CMD [ "tests/test_runner.py" ]