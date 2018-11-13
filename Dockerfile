FROM python:3-alpine

COPY requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt

RUN apk add --no-cache dumb-init

COPY prometheus_speedtest/ /prometheus_speedtest/

EXPOSE 9516/tcp
ENTRYPOINT [ \
    "dumb-init", "python", "-m", "prometheus_speedtest.prometheus_speedtest" \
]
CMD [ "--port=9516" ]
