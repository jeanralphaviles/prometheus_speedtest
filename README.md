# Prometheus Speedtest

Instrument [Speedtest.net](http://speedtest.net) tests from
[Prometheus](https://prometheus.io). Provides metrics on download\_speed,
upload\_speed, and latency.

[![Build Status](https://travis-ci.org/jeanralphaviles/prometheus_speedtest.svg?branch=master)](https://travis-ci.org/jeanralphaviles/prometheus_speedtest/branches)
[![Docker Build Status](https://img.shields.io/docker/build/jraviles/prometheus_speedtest.svg)](https://hub.docker.com/r/jraviles/prometheus_speedtest/)
[![PyPI status](https://img.shields.io/pypi/status/prometheus_speedtest.svg)](https://pypi.python.org/pypi/prometheus_speedtest/)
[![PyPI version shields.io](https://img.shields.io/pypi/v/prometheus_speedtest.svg)](https://pypi.python.org/pypi/prometheus_speedtest/)
[![PyPI license](https://img.shields.io/pypi/l/prometheus_speedtest.svg)](https://pypi.python.org/pypi/prometheus_speedtest/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/prometheus_speedtest.svg)](https://pypi.python.org/pypi/prometheus_speedtest/)

![Grafana](https://github.com/jeanralphaviles/prometheus_speedtest/raw/master/images/grafana.png)

## Getting Started

These instructions will install and run `prometheus_speedtest` on your system.

### PyPi Package

`prometheus_speedtest` is provided as a
[PyPi package](https://pypi.org/project/prometheus_speedtest).

1. Installing

   ```shell
   pip3 install prometheus_speedtest
   ```

1. Running

   ```shell
   prometheus_speedtest
   ```

#### Usage

```
usage: prometheus_speedtest [-h] [-d] [-p port]

Instrument speedtest.net speedtests from Prometheus.

optional arguments:
  -h, --help            show this help message and exit
  -d, --daemon          Run prometheus_speedtest in the background. (default:
                        False)
  -p port, --port port  port to listen on. (default: 8080)
```

### Running with Docker

`prometheus_speedtest` is also available as a [Docker](http://docker.com) image
on [Docker Hub](https://hub.docker.com/r/jraviles/prometheus_speedtest)
:whale:.

```shell
docker run --rm -d --name prometheus_speedtest -p 8080:8080/tcp jraviles/prometheus_speedtest:latest
```

### Integrating with Prometheus

`prometheus_speedtest` is best when paired with
[Prometheus](https://prometheus.io). Prometheus can be configured to perform
Speedtests on an interval and record their results.

Speedtest metrics available to query in Prometheus.

| Metric Name           | Description                 |
|---------------------- |---------------------------- |
| download\_speed\_bps  | Download speed (bit/s)      |
| upload\_speed\_bps    | Upload speed (bit/s)        |
| ping\_ms              | Latency (ms)                |
| bytes\_received       | Bytes received during test  |
| bytes\_sent           | Bytes sent during test      |

#### prometheus.yml config

Add this to your
[Prometheus config](https://prometheus.io/docs/prometheus/latest/configuration/configuration)
to start instrumenting Speedtests and recording their metrics.

```yaml
global:
  scrape_timeout: 60s

scrape_configs:
- job_name: 'speedtest'
  metrics_path: /probe
  static_configs:
  - targets:
    - localhost:8080
```

Note if you're running `prometheus` under Docker, you must link the
`prometheus` container to `prometheus_speedtest`. See the steps below for how
this can be done.

#### Trying it out

An example
[Prometheus config](https://prometheus.io/docs/prometheus/latest/configuration/configuration)
has been provided at
[example/prometheus.yml](https://github.com/jeanralphaviles/prometheus_speedtest/blob/master/example/prometheus.yml).
We'll start `prometheus` with this config.

1. Docker Network

   Create the [Docker network](https://docs.docker.com/network) that will link
   `prometheus_speedtest` and `prometheus` together.

   ```shell
   docker network create prometheus_network
   ```

1. Start Prometheus Speedtest

   ```shell
   docker run --rm -d --net prometheus_network -p 8080:8080/tcp \
      --name prometheus_speedtest jraviles/prometheus_speedtest:latest
   ```

1. Start Prometheus

   ```shell
   docker run --rm -d --net prometheus_network -p 9090:9090/tcp \
      -v $PWD/example/prometheus.yml:/etc/prometheus/prometheus.yml \
      --name prometheus prom/prometheus:latest
   ```

1. Query results

   * Visit <http://localhost:9090>

   * Wait around **45 seconds** for Prometheus to perform a Speedtest

   * Issue a query for **download\_speed\_bps**

     You should see something like this.

     ![Prometheus Query](https://github.com/jeanralphaviles/prometheus_speedtest/raw/master/images/query.png)

### Instrumenting Speedtests with cURL

Once `prometheus_speedtest` has been started, with either Docker or PyPi,
Speedtests can be instrumented with [cURL](https://curl.haxx.se).

```shell
$ curl localhost:8080/probe
# HELP download_speed_bps Download speed (bit/s)
# TYPE download_speed_bps gauge
download_speed_bps 88016694.95692767
# HELP upload_speed_bps Upload speed (bit/s)
# TYPE upload_speed_bps gauge
upload_speed_bps 3415613.277989314
# HELP ping_ms Latency (ms)
# TYPE ping_ms gauge
ping_ms 20.928
# HELP bytes_received Bytes received during test
# TYPE bytes_received gauge
bytes_received 111342756.0
# HELP bytes_sent Bytes sent during test
# TYPE bytes_sent gauge
bytes_sent 5242880.0
```

You can also visit <http://localhost:8080> in your browser to see the same
metrics.

## Getting Started (Development)

These instructions will get you a copy `prometheus_speedtest` up and running on
your local machine for development and testing purposes.

### Prerequisites

* [Python 3](https://www.python.org)
* [Docker](https://www.docker.com)
* [Pytest](https://pytest.org)

### Running Locally

#### Python

1. Ensure packages listed in
   [requirements.txt](https://github.com/jeanralphaviles/prometheus_speedtest/blob/master/requirements.txt)
   are installed with `pip3`

   ```python
   pip3 install -r requirements.txt
   ```

1. Run `prometheus_speedtest`

   ```python
   python3 prometheus_speedtest/prometheus_speedtest.py
   ```

#### Docker

1. Building image

   ```shell
   docker build -t prometheus_speedtest:latest .
   ```

1. Running

   ```shell
   docker run --rm -d --name prometheus_speedtest -p 8080:8080/tcp prometheus_speedtest:latest
   ```

### Perform a Speedtest

```shell
curl localhost:8080/probe
```

Or visit <http://localhost:8080>

### Running Unit Tests

```shell
pytest-3
```

### Contributing

Pull requests are welcome. Please adhere to the
[Google Python style guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md).

Please format your contributions with the
[yapf](https://github.com/google/yapf) formatter and lint your code with
[pylint](https://www.pylint.org). A
[.pylintrc](https://github.com/jeanralphaviles/prometheus_speedtest/blob/master/.pylintrc)
config has been provided.

```shell
yapf -i **/*.py
pylint3 **/*.py
```

## Maintenance

### Deploying to PyPi

1. Increment version number in
   [version.txt](https://github.com/jeanralphaviles/prometheus_speedtest/blob/master/version.txt)

1. Create PyPi package

   ```shell
   python3 setup.py sdist
   ```

1. Upload package to PyPi

   Ensure that [Twine](https://github.com/pypa/twine) has been installed.

   ```shell
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
* Ben Finney [python-daemon](https://pypi.org/project/python-daemon)
