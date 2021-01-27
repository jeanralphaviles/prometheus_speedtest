FROM alpine:latest as compiler

RUN apk add --no-cache alpine-sdk cmake curl-dev libxml2-dev

WORKDIR /build
RUN git clone https://github.com/taganaka/SpeedTest.git . \
  && cmake -DCMAKE_BUILD_TYPE=Release . \
  && make


FROM python:3.7-alpine

COPY requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt

RUN apk add --no-cache dumb-init libcurl libxml2 libstdc++ libgcc

COPY prometheus_speedtest/ /prometheus_speedtest/
COPY --from=compiler /build/SpeedTest /usr/local/bin/SpeedTest

EXPOSE 9516/tcp
ENTRYPOINT [ \
    "python", "-m", "prometheus_speedtest.prometheus_speedtest" \
]
CMD [ "--port=9516" ]
