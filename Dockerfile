FROM python:3.7

COPY prometheus_speedtest.py /
COPY requirements.txt /

RUN [ "pip", "install", "--no-cache-dir", "-r", "requirements.txt" ]

EXPOSE 8080/tcp
ENTRYPOINT [ "python", "prometheus_speedtest.py" ]
CMD [ "--port=8080" ]
