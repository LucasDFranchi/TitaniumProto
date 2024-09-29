FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
    git \
    python3 \
    python3-pip \
    protobuf-compiler \
    # dos2unix \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/output/
RUN mkdir -p /app/tmp/
WORKDIR /app

RUN git clone https://github.com/nanopb/nanopb.git /app/nanopb

COPY ./src/* /app/

RUN chmod +x ./entrypoint.sh

RUN pip3 install nanopb
RUN pip3 install protobuf==3.20.0

ENTRYPOINT [ "/app/entrypoint.sh" ]

CMD [ "echo", "Default argument from CMD instruction" ]
