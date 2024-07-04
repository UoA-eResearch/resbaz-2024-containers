FROM debian:bookworm-slim

RUN apt-get update \
    && apt-get install -y git make g++ zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/haghshenas/fastutils.git /tmp/fastutils \
    && cd /tmp/fastutils \
    && make \
    && cp fastutils /usr/local/bin \
    && rm -rf /tmp/fastutils

WORKDIR /app

CMD ["/usr/local/bin/fastutils"]
