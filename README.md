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

```
docker run --rm -d --name prometheus_speedtest -p 8080:8080/tcp jraviles/prometheus_speedtest:latest
```

### Installing with PyPi

prometheus\_speedtest is also provided as a
[PyPi package](https://pypi.org/project/prometheus_speedtest). It can be
installed with:

```
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

## Getting Started (Development)

These instructions will get you a copy of the project up and running on your
local machine for development and testing purposes. See deployment for notes on
how to deploy the project on a live system.

### Prerequisites

* [Python 2.7](https://www.python.org)
* [Docker](https://www.docker.com)
* [Twine](https://github.com/pypa/twine)

### Running locally

First, ensure packages listed in requirements.txt are installed with pip.

```
python2 prometheus_speedtest.py
```

### Running with Docker

```
docker build -t prometheus_speedtest:latest .
docker run --rm -d -p 8080:8080/tcp prometheus_speedtest:latest
```

### Perform a Speedtest

```
curl localhost:8080/probe
```

Or visit http://localhost:8080

### Testing 

```
python2 prometheus_speedtest_test.py
```

### Contributing

Pull requests welcome. Please adhere to the
[Google Python style guide.](https://google.github.io/styleguide/pyguide.html)

### Deploying

#### pypi

```
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
