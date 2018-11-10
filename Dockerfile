FROM python:3.7-alpine

COPY requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt

RUN apk add --no-cache dumb-init

COPY prometheus_speedtest.py /

EXPOSE 8080/tcp
ENTRYPOINT [ "dumb-init", "python", "prometheus_speedtest.py" ]
CMD [ "--port=8080" ]
