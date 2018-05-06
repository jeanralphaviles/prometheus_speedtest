# Prometheus Speedtest

Performs [Speedtest.net](http://speedtest.net) tests and pushes their results
to Prometheus Pushgateway.

## Getting Started

These instructions will install `prometheus_speedtest` on your system.

### Prerequisites

* [Python 2.7 - 3.6](https://www.python.org)
* [python-pip](https://packaging.python.org/tutorials/installing-packages)

### Installing

```
pip install prometheus_speedtest
```

### Running

```
prometheus_speedtest.par
```

### Usage

```
usage: prometheus_speedtest.par [-h] [-s addr] [-t sec] [-p host:port]
                                [-n name]

Export speedtest metrics to Prometheus Pushgateway.

optional arguments:
  -h, --help            show this help message and exit
  -s addr, --source_address addr
                        IP address for speedtest to bind to.
  -t sec, --timeout sec
                        Speedtest timeout, seconds.
  -p host:port, --pushgateway host:port
                        Address of Prometheus Pushgateway.
  -n name, --name name  Job name to report Prometheus metrics as.
```

## Getting Started (Development)

These instructions will get you a copy of the project up and running on your
local machine for development and testing purposes. See deployment for notes on
how to deploy the project on a live system.

### Prerequisites

* [Python 2.7 - 3.6](https://www.python.org)
* [Bazel](https://bazel.build)

### Compiling

```
bazel build //:prometheus_speedtest
```

### Running
```
bazel run //:prometheus_speedtest
```

### Testing
```
bazel test //:prometheus_speedtest_test
```

### Contributing

Pull requests welcome. Please adhere to the
[Google Python style guide.](https://google.github.io/styleguide/pyguide.html)

### Deploying

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
