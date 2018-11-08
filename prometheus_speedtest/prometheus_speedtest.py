#!/usr/bin/python3
"""Instrument speedtest.net speedtests from Prometheus."""

from __future__ import print_function

import os
from absl import app
from absl import flags
from absl import logging
from prometheus_client import core
import prometheus_client
import speedtest

from . import version

try:
    from http.server import HTTPServer
    from http.server import SimpleHTTPRequestHandler
    from socketserver import ThreadingMixIn
    from urllib.parse import urlparse
except ImportError:
    # Python 2
    from BaseHTTPServer import HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from SocketServer import ThreadingMixIn
    from urlparse import urlparse

flags.DEFINE_string('address', '0.0.0.0', 'address to listen on')
flags.DEFINE_integer('port', 9516, 'port to listen on')
flags.DEFINE_boolean('version', False, 'show version')
FLAGS = flags.FLAGS


class PrometheusSpeedtest():
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
        client = speedtest.Speedtest(source_address=self._source_address,
                                     timeout=self._timeout)
        client.get_best_server()
        client.download()
        client.upload()
        logging.info(client.results)
        return client.results


class SpeedtestCollector():
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


class _ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    """Thread per request HTTP server.

    http.server.ThreadingHTTPServer is new to Python 3.7, create our own for
    backwards-compatibility.
    """
    # Allow Python to exit before all threads have terminated. This speeds up
    # shutdown and also prevents a memory leak as Python is keeping track of
    # all threads ever spawned.
    daemon_threads = True


class SpeedtestMetricsHandler(SimpleHTTPRequestHandler,
                              prometheus_client.MetricsHandler):
    """HTTP handler extending MetricsHandler and adding status page support."""
    def do_GET(self):
        """Handles HTTP GET requests.

        Requests to '/probe' are handled by prometheus_client.MetricsHandler,
        other requests serve static HTML.
        """
        path = urlparse(self.path).path
        if path == '/probe':
            prometheus_client.MetricsHandler.do_GET(self)
        else:
            SimpleHTTPRequestHandler.do_GET(self)


def main(argv):
    """Entry point for prometheus_speedtest.py."""
    del argv  # unused
    if FLAGS.version:
        print('prometheus_speedtest v%s' % version.__version__)
        return

    registry = core.CollectorRegistry(auto_describe=False)
    registry.register(SpeedtestCollector())
    metrics_handler = SpeedtestMetricsHandler.factory(registry)

    server = _ThreadingSimpleServer((FLAGS.address, FLAGS.port),
                                    metrics_handler)
    # SimpleHTTPRequestHandler added support for a directory argument in Python
    # 3.7. Change directory here for backwards compatibility with older
    # versions of Python.
    os.chdir(os.path.join(os.path.dirname(__file__), 'static'))

    logging.info('Starting HTTP server listening on %s:%s', FLAGS.address,
                 FLAGS.port)
    server.serve_forever()


if __name__ == '__main__':
    app.run(main)
