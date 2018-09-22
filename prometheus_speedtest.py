"""Instrument speedtest.net speedtests from Prometheus."""

import BaseHTTPServer
import argparse
import multiprocessing
import urlparse

import glog as log
import prometheus_client

import speedtest

PARSER = argparse.ArgumentParser(
    description='Instrument speedtest.net speedtests from Prometheus.')
PARSER.add_argument(
    '-p', '--port', metavar='port', default=8080, type=int,
    help='port to listen on.')


class Error(Exception):
  """Base class for exceptions raised in this module."""


class TimeoutError(Exception):
  """Speedtest timeout."""


# Global function for multiprocessing library.
def _perform_test(source_address):
  """Performs a speedtest."""
  client = speedtest.Speedtest(source_address=source_address)
  client.get_best_server()
  client.download()
  client.upload()
  return client


class PrometheusSpeedtest(object):
  """Enapsulates behavior performing and reporting results of speedtests."""

  def __init__(self, source_address=None, timeout=60):
    """Instantiates a PrometheusSpeedtest object.

    Args:
      source_address: str - optional network address to bind to.
        e.g. 192.168.1.1.
      timeout: int - optional timeout for speedtest in seconds.
    """
    self.source_address = source_address
    self.timeout = int(timeout)

  def _test(self):
    """Performs speedtest, returns results.

    Returns:
      speedtest.SpeedtestResults object.
    Raises:
      TimeoutError: Speedtest timeout was reached.
    """
    pool = multiprocessing.Pool(processes=1)
    async_result = pool.apply_async(_perform_test, args=(self.source_address,))
    try:
      speedtest_client = async_result.get(self.timeout)
      return speedtest_client.results
    except multiprocessing.TimeoutError:
      raise TimeoutError('Speedtest timeout')

  def _metrics(self, results):
    """Produces Prometheus metrics from Speedtest results.

    Args:
      results: speedtest.SpeedtestResults object.
    Returns:
      prometheus_client.CollectorRegistry containing metrics.
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
    bytes_sent = prometheus_client.Gauge(
        'bytes_sent', 'Bytes sent during test', registry=registry)
    bytes_sent.set(results.bytes_sent)
    bytes_received = prometheus_client.Gauge(
        'bytes_received', 'Bytes received during test', registry=registry)
    bytes_received.set(results.bytes_received)

    return registry

  def report(self):
    """Performs a speedtest and returns Prometheus metrics.

    Returns:
      prometheus_client.CollectorRegistry containing metrics.
    """
    results = self._test()
    return self._metrics(results)


class HTTPHandler(prometheus_client.MetricsHandler):
  """Handles HTTP Requests."""

  def do_GET(self):
    """Handles HTTP Get requests."""
    log.info('Handling request "%s"', self.path)
    if self.path.startswith('/probe'):
      params = {
          k: v[0] for k, v in
          urlparse.parse_qs(urlparse.urlparse(self.path).query).items()
      }
      tester = PrometheusSpeedtest(**params)
      try:
        self.registry = tester.report()
      except Exception as e:
        log.error(e)
        self.send_response(500)
        self.end_headers()
        log.warn('Response code 500')
        return
      prometheus_client.MetricsHandler.do_GET(self)
      log.info('Response code 200')
    else:
      with open('static/usage.html', 'r') as f:
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(f.read()))
        self.end_headers()
        f.seek(0)
        self.wfile.write(f.read())


def main():
  """Entry point for prometheus_speedtest.py."""
  flags = PARSER.parse_args()
  server = BaseHTTPServer.HTTPServer(('', flags.port), HTTPHandler)
  log.info('Listening on port %s', flags.port)
  server.serve_forever()


if __name__ == '__main__':
  main()
