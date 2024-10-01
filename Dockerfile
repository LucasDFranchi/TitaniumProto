FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
    git \
    python3 \
    python3-pip \
    protobuf-compiler \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/output/
RUN mkdir -p /app/tmp/
RUN mkdir -p /app/resources/
WORKDIR /app

RUN git clone https://github.com/nanopb/nanopb.git /app/nanopb

COPY ./src/cli.py /app/
COPY ./src/resources/* /app/resources/

RUN pip3 install nanopb
RUN pip3 install protobuf==3.20.0