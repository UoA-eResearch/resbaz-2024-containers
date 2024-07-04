FROM alpine:3.20

ARG OPENBABEL_REF=master

RUN apk --no-cache add \
    git \
    g++ cmake make perl \
    boost-dev cairo-dev eigen-dev libxml2-dev zlib-dev

RUN git clone https://github.com/openbabel/openbabel.git /tmp/openbabel \
    && cd /tmp/openbabel \
    && git checkout ${OPENBABEL_REF} \
    && env CXXFLAGS="-Wno-deprecated-declarations" cmake . \
    && make -j2 \
    && make install \
    && rm -rf /tmp/openbabel

ENTRYPOINT ["/usr/local/bin/obabel"]
CMD [""]
