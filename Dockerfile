FROM python:3.8


RUN mkdir -p /source/fastwriting
WORKDIR /source/fastwriting
ENV PYTHONPATH=/source/fastwriting

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

ADD . ./