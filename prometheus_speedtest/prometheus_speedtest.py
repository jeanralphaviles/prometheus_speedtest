#!/usr/bin/python3
"""Instrument speedtest.net speedtests from Prometheus."""

import argparse
import http
import socketserver

import glog as logging
import prometheus_client
from prometheus_client import core
import speedtest

from prometheus_speedtest import version

PARSER = argparse.ArgumentParser(
    description='Instrument speedtest.net speedtests from Prometheus.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
PARSER.add_argument(
    '-p',
    '--port',
    metavar='port',
    default=8080,
    type=int,
    help='port to listen on')
PARSER.add_argument(
    '-v',
    '--version',
    action='version',
    version='%(prog)s v{version}'.format(version=version.__version__),
    help='show version information and exit')

FLAGS = PARSER.parse_args()


class PrometheusSpeedtest:
    """Enapsulates behavior performing and reporting results of speedtests."""

    def __init__(self, source_address=None, timeout=10):
        """Instantiates a PrometheusSpeedtest object.

        Args:
            source_address: str - optional network address to bind to.
                e.g. 192.168.1.1.
            timeout: int - optional timeout for speedtest in seconds.
        """
        self._source_address = source_address
        self._timeout = timeout

    def test(self):
        """Performs speedtest, returns results.

        Returns:
            speedtest.SpeedtestResults object.
        """
        logging.info('Performing Speedtest')
        client = speedtest.Speedtest(
            source_address=self._source_address, timeout=self._timeout)
        client.get_best_server()
        client.download()
        client.upload()
        logging.info(client.results)
        return client.results


class SpeedtestCollector:
    """Performs Speedtests when requested from Prometheus."""

    def __init__(self, tester=None):
        """Instantiates a SpeedtestCollector object.

        Args:
            tester: An instantiated PrometheusSpeedtest object for testing.
        """
        self._tester = tester if tester else PrometheusSpeedtest()

    def collect(self):
        """Performs a Speedtests and yields metrics.

        Yields:
            core.Metric objects.
        """
        results = self._tester.test()

        download_speed = core.GaugeMetricFamily('download_speed_bps',
                                                'Download speed (bit/s)')
        download_speed.add_metric(labels=[], value=results.download)
        yield download_speed

        upload_speed = core.GaugeMetricFamily('upload_speed_bps',
                                              'Upload speed (bit/s)')
        upload_speed.add_metric(labels=[], value=results.upload)
        yield upload_speed

        ping = core.GaugeMetricFamily('ping_ms', 'Latency (ms)')
        ping.add_metric(labels=[], value=results.ping)
        yield ping

        bytes_received = core.GaugeMetricFamily('bytes_received',
                                                'Bytes received during test')
        bytes_received.add_metric(labels=[], value=results.bytes_received)
        yield bytes_received

        bytes_sent = core.GaugeMetricFamily('bytes_sent',
                                            'Bytes sent during test')
        bytes_sent.add_metric(labels=[], value=results.bytes_sent)
        yield bytes_sent


def main():
    """Entry point for prometheus_speedtest.py."""
    registry = core.CollectorRegistry(auto_describe=False)
    registry.register(SpeedtestCollector())
    metrics_handler = prometheus_client.MetricsHandler.factory(registry)

    # http.server.ThreadingHTTPServer is new to Python 3.7, create our own for
    # backwards-compatibility.
    threading_http_server = type(
        'ThreadingHTTPServer',
        (socketserver.ThreadingMixIn, http.server.HTTPServer), {})
    server = threading_http_server(('', FLAGS.port), metrics_handler)

    logging.info('Starting HTTP server on port %s', FLAGS.port)
    server.serve_forever()


if __name__ == '__main__':
    main()
