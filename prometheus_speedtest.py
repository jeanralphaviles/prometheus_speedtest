"""Performs speedtest-cli tests and pushes results to Prometheus Pushgateway."""

import argparse

import speedtest

class PrometheusSpeedtest(object):
  """Enapsulates behavior performing and reporting results of speedtests."""

  def __init__(self, source_address, timeout, *args, **kwargs):
    """Instantiates a PrometheusSpeedtest object.

    Args:
      source_address: str - optional network address to bind to.
        e.g. 192.168.1.1.
      timeout: int - optional timeout for speedtest in seconds.
    """
    super(PrometheusSpeedtest, self).__init__(*args, **kwargs)
    self.source_address = source_address
    self.timeout = timeout

  def test(self):
    """Performs speedtest, returns results.

    Returns:
    """
    client = speedtest.Speedtest(
        source_address=self.source_address, timeout=self.timeout)
    client.get_best_server()
    client.download()
    client.upload()
    return client.results.dict()

def parse_args():
  """Parses and returns command-line flags."""
  parser = argparse.ArgumentParser(
      description='Export speedtest metrics to Prometheus Pushgateway.')
  parser.add_argument('-a', '--source_address', metavar='ADDR', type=str)
  parser.add_argument('-t', '--timeout', metavar='SEC', default=10, type=int)
  return parser.parse_args()


def main():
  """Entry point for prometheus_speedtest.py."""
  args = parse_args()
  tester = PrometheusSpeedtest(args.source_address, args.timeout)
  print(tester.test())


if __name__ == '__main__':
  main()
