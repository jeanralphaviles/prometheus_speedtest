"""Performs speedtest-cli tests and pushes results to Prometheus Pushgateway."""

import argparse
import socket
import threading

import prometheus_client
import speedtest

PARSER = argparse.ArgumentParser(
    description='Export speedtest metrics to Prometheus Pushgateway.')
PARSER.add_argument(
    '-s', '--source_address', metavar='addr', type=str,
    help='IP address for speedtest to bind to.')
PARSER.add_argument(
    '-t', '--timeout', metavar='sec', default=30, type=int,
    help='Speedtest timeout, seconds.')
PARSER.add_argument(
    '-p', '--pushgateway', metavar='host:port', default='localhost:9091',
    type=str, help='Address of Prometheus Pushgateway.')
PARSER.add_argument(
    '-n', '--name', metavar='name', default='prometheus_speedtest', type=str,
    help='Job name to report Prometheus metrics as.')


class Error(Exception):
  """Base class for exceptions raised in this module."""


class TimeoutError(Exception):
  """Speedtest timeout."""


class PrometheusSpeedtest(object):
  """Enapsulates behavior performing and reporting results of speedtests."""

  def __init__(self, pushgateway, jobname, source_address=None, timeout=None,
               *args, **kwargs):
    """Instantiates a PrometheusSpeedtest object.

    Args:
      pushgateway: str - host:port of Prometheus Pushgateway.
      jobname: str - jobname to report to Prometheus Pushgateway.
      source_address: str - optional network address to bind to.
        e.g. 192.168.1.1.
      timeout: int - optional timeout for speedtest in seconds.
    """
    super(PrometheusSpeedtest, self).__init__(*args, **kwargs)
    self.pushgateway = pushgateway
    self.jobname = jobname
    self.source_address = source_address
    self.timeout = timeout

  def _test(self):
    """Performs speedtest, returns results.

    Returns:
      speedtest.SpeedtestResults object.
    Raises:
      TimeoutError: Speedtest timeout was reached.
    """
    client = speedtest.Speedtest(source_address=self.source_address)

    def perform_test(client):
      """Performs speedtest."""
      client.get_best_server()
      client.download()
      client.upload()

    thread = threading.Thread(target=perform_test, args=(client,))
    thread.start()
    thread.join(self.timeout)
    if thread.is_alive():
      raise TimeoutError('Speedtest timeout')
    return client.results

  def _push(self, results):
    """Pushes metrics about a speedtest to the Prometheus Pushgateway.

    Args:
      results: speedtest.SpeedtestResults object.
    """
    registry = prometheus_client.CollectorRegistry()
    download_bps = prometheus_client.Gauge(
        'download_speed_bps', 'Download speed (bit/s)',
        registry=registry)
    download_bps.set(results.download)
    upload_bps = prometheus_client.Gauge(
        'upload_speed_bps', 'Upload speed (bit/s)', registry=registry)
    upload_bps.set(results.upload)
    ping = prometheus_client.Gauge(
        'ping_ms', 'Latency (ms)', registry=registry)
    ping.set(results.ping)

    grouping_key = {
        'instance': socket.gethostname(),
    }

    prometheus_client.push_to_gateway(
        self.pushgateway, job=self.jobname, grouping_key=grouping_key,
        registry=registry)

  def report(self):
    """Performs a speedtest and pushes metrics to Prometheus Pushgateway."""
    results = self._test()
    self._push(results)


def main():
  """Entry point for prometheus_speedtest.py."""
  flags = PARSER.parse_args()
  tester = PrometheusSpeedtest(
      flags.pushgateway, flags.name, flags.source_address, flags.timeout)
  tester.report()


if __name__ == '__main__':
  main()
