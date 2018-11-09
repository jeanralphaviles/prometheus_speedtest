# Prometheus Speedtest

Instrument [Speedtest.net](http://speedtest.net) tests from Prometheus.

[![Docker Build Status](https://img.shields.io/docker/build/jraviles/prometheus_speedtest.svg)](https://hub.docker.com/r/jraviles/prometheus_speedtest/)
[![PyPI status](https://img.shields.io/pypi/status/prometheus_speedtest.svg)](https://pypi.python.org/pypi/prometheus_speedtest/)
[![PyPI version shields.io](https://img.shields.io/pypi/v/prometheus_speedtest.svg)](https://pypi.python.org/pypi/prometheus_speedtest/)
[![PyPI license](https://img.shields.io/pypi/l/prometheus_speedtest.svg)](https://pypi.python.org/pypi/prometheus_speedtest/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/prometheus_speedtest.svg)](https://pypi.python.org/pypi/prometheus_speedtest/)

![Grafana](https://github.com/jeanralphaviles/prometheus_speedtest/raw/master/images/grafana.png)


## Getting Started

These instructions will run `prometheus_speedtest` on your system.

### Running with Docker

prometheus\_speedtest is available on
[Docker Hub](https://hub.docker.com/r/jraviles/prometheus_speedtest) :whale:.

```shell
docker run --rm -d --name prometheus_speedtest -p 8080:8080/tcp jraviles/prometheus_speedtest:latest
```

### Installing with PyPi

prometheus\_speedtest is also provided as a
[PyPi package](https://pypi.org/project/prometheus_speedtest). It can be
installed with:

```shell
pip install prometheus_speedtest
```

### Usage

```
usage: prometheus_speedtest.py [-h] [-p port]

Instrument speedtest.net speedtests from Prometheus.

optional arguments:
  -h, --help            show this help message and exit
  -p port, --port port  port to listen on.
```

### Integrating with Prometheus

#### Example prometheus.yml config

```yaml
global:
  scrape_timeout: 60s

scrape_configs:
- job_name: 'speedtest'
  metrics_path: /probe
  static_configs:
  - targets:
    - prometheus_speedtest:8080
```

#### Trying it out

An example config has been provided at
[example/prometheus.yml](https://github.com/jeanralphaviles/prometheus_speedtest/blob/master/example/prometheus.yml).

```shell
docker network create prometheus_network
docker run --rm -d --net prometheus_network -p 8080:8080/tcp --name prometheus_speedtest \
    jraviles/prometheus_speedtest:latest
docker run --rm -d --net prometheus_network -p 9090:9090/tcp \
    -v $PWD/example/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus:latest
```

Visit http://localhost:9090, wait for Prometheus to scrape, and issue a query
for **download\_speed\_bps**. You should see something like this.

![Prometheus Query](https://github.com/jeanralphaviles/prometheus_speedtest/raw/master/images/query.png)

## Getting Started (Development)

These instructions will get you a copy of the project up and running on your
local machine for development and testing purposes. See deployment for notes on
how to deploy the project on a live system.

### Prerequisites

* [Python 3.7](https://www.python.org)
* [Docker](https://www.docker.com)
* [Twine](https://github.com/pypa/twine)

### Running locally

First, ensure packages listed in requirements.txt are installed with pip.

```
python3 prometheus_speedtest.py
```

### Running with Docker

```shell
docker build -t prometheus_speedtest:latest .
docker run --rm -d --name prometheus_speedtest -p 8080:8080/tcp prometheus_speedtest:latest
```

### Perform a Speedtest

```shell
curl localhost:8080
```

Or visit http://localhost:8080

### Testing 

```shell
python3 prometheus_speedtest_test.py
```

### Contributing

Pull requests welcome. Please adhere to the
[Google Python style guide.](https://google.github.io/styleguide/pyguide.html)

### Deploying

#### pypi

```shell
python3 setup.py sdist
twine upload dist/*
```

## Authors

* Jean-Ralph Aviles

## License

This product is licensed under the Apache 2.0 license. See [LICENSE](LICENSE)
file for details.

## Acknowledgments

* Matt Martz [speedtest-cli](https://github.com/sivel/speedtest-cli)
* The Prometheus team <https://prometheus.io>
* Testing in Python team <http://lists.idyll.org/listinfo/testing-in-python>
* Benjamin Staffin [python-glog](https://github.com/benley/python-glog)
