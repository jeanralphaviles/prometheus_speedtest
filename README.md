# Prometheus Speedtest

Instrument [Speedtest.net](http://speedtest.net) tests from Prometheus.

[![PyPI status](https://img.shields.io/pypi/status/prometheus_speedtest.svg)](https://pypi.python.org/pypi/prometheus_speedtest/) [![PyPI version shields.io](https://img.shields.io/pypi/v/prometheus_speedtest.svg)](https://pypi.python.org/pypi/prometheus_speedtest/) [![PyPI license](https://img.shields.io/pypi/l/prometheus_speedtest.svg)](https://pypi.python.org/pypi/prometheus_speedtest/) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/prometheus_speedtest.svg)](https://pypi.python.org/pypi/prometheus_speedtest/)

## Getting Started

These instructions will install `prometheus_speedtest` on your system.

### Prerequisites

* [Python 2.7](https://www.python.org)
* [python-pip](https://packaging.python.org/tutorials/installing-packages)

### Installing

```
pip install prometheus_speedtest
```

### Running

```
prometheus_speedtest
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
* [Bazel](https://bazel.build)
* [Docker](https://www.docker.com)
* [Twine](https://github.com/pypa/twine)

### Compiling with Bazel

```
bazel build //:prometheus_speedtest
```

### Running with Bazel

```
bazel run //:prometheus_speedtest
```

### Running without Bazel

First, ensure packages listed in requirements.txt are installed with pip.

```
python2 prometheus_speedtest.py
```

### Running with Docker

1. Using Bazel-Docker integration

[Documentation](https://github.com/bazelbuild/rules_docker)

```
bazel run //:prometheus_speedtest_image
```

2. Raw Docker

```
docker build -t prometheus_speedtest:latest .
docker run --rm -d -p 8080:8080/tcp prometheus_speedtest:latest
```

### Perform a Speedtest

```
curl localhost:8080/probe
```

Or visit http://localhost:8080

### Testing with Bazel

```
bazel test //:prometheus_speedtest_test
```

### Testing without Bazel

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

#### par\_binary

```
bazel build //:prometheus_speedtest.par
cp "$(bazel info bazel-bin)/prometheus_speedtest.par" ...
```

See <https://github.com/google/subpar> or <https://google.github.io/subpar> for
documentation on Python `.par` files.

#### Debian package

```
bazel build //:prometheus_speedtest-debian
sudo apt install "$(bazel info bazel-bin)/prometheus_speedtest-debian.deb"
/usr/bin/prometheus_speedtest.par
```

If reinstalling package, remember to increment the number in `version.txt`.
Otherwise apt will believe the package hasn't changed and will refuse to
install a new version.

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
