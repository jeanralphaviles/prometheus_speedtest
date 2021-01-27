#!/usr/bin/python3.7
"""Instrument speedtest.net speedtests from Prometheus."""

from typing import Optional
from typing import Sequence
from http import server
from urllib.parse import urlparse
import os

from absl import app
from absl import flags
from absl import logging
from prometheus_client import core
import prometheus_client

from prometheus_speedtest import version

flags.DEFINE_string('address', '0.0.0.0', 'address to listen on')
flags.DEFINE_integer('port', 9516, 'port to listen on')
flags.DEFINE_list(
    'servers', [],
    'speedtest server(s) to use - leave empty for auto-selection')
flags.DEFINE_list(
    'excludes', [],
    'speedtest server(s) to exclude - leave empty for no exclusion')
flags.DEFINE_boolean('version', False, 'show version')
FLAGS = flags.FLAGS


class PrometheusSpeedtest():
    """Enapsulates behavior performing and reporting results of speedtests."""
    def __init__(self,
                 source_address: Optional[str] = None,
                 timeout: int = 10,
                 servers: Optional[Sequence[str]] = None,
                 excludes: Optional[Sequence[str]] = None):
        """Instantiates a PrometheusSpeedtest object.

        Args:
            source_address: str - optional network address to bind to.
                e.g. 192.168.1.1.
            timeout: int - optional timeout for speedtest in seconds.
            servers: list of speedtest server ids to restrict testing to.
            servers: list of speedtest server ids to exclude testing from.
        """
        self._source_address = source_address
        self._timeout = timeout
        self._servers = servers
        self._excludes = excludes

    def test(self):
        """Performs speedtest, returns results.

        Returns:
            speedtest.SpeedtestResults object.
        """
        logging.info('Performing Speedtest...')
        res = subprocess.run(["./SpeedTest", "--output", "json"], capture_output=True, stdin=None)
        if res.returncode != 0:
          logging.error('Error running SpeedTest: %s', res.stderr)
        results = json.loads(res.stdout.decode())
        logging.debug('Picked server: %s by %s (%.2f km, %.2f ping)', results['server']['name'], results['server']['sponsor'], results['server']['d'], results['server']['latency'])
        logging.info('Results: %s', results)
        return results


class SpeedtestCollector():
    """Performs Speedtests when requested from Prometheus."""
    def __init__(self,
                 tester: Optional[PrometheusSpeedtest] = None,
                 servers: Optional[Sequence[str]] = None,
                 excludes: Optional[Sequence[str]] = None):
        """Instantiates a SpeedtestCollector object.

        Args:
            tester: An instantiated PrometheusSpeedtest object for testing.
            servers: servers-id to use when tester is auto-created
        """
        self._tester = tester if tester else PrometheusSpeedtest(
            servers=servers, excludes=excludes)

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


class SpeedtestMetricsHandler(server.SimpleHTTPRequestHandler,
                              prometheus_client.MetricsHandler):
    """HTTP handler extending MetricsHandler and adding status page support."""
    def __init__(self, *args, **kwargs):
        static_directory = os.path.join(os.path.dirname(__file__), 'static')
        # pylint: disable=unexpected-keyword-arg
        super().__init__(directory=static_directory, *args, **kwargs)
        # pylint: enable=unexpected-keyword-arg

    def do_GET(self):
        """Handles HTTP GET requests.

        Requests to '/probe' are handled by prometheus_client.MetricsHandler,
        other requests serve static HTML.
        """
        logging.info('%s - %s', self.requestline, self.client_address)
        path = urlparse(self.path).path
        if path == '/probe':
            prometheus_client.MetricsHandler.do_GET(self)
        else:
            server.SimpleHTTPRequestHandler.do_GET(self)


def main(argv):
    """Entry point for prometheus_speedtest.py."""
    del argv  # unused
    if FLAGS.version:
        print('prometheus_speedtest v%s' % version.VERSION)
        return

    registry = core.CollectorRegistry(auto_describe=False)
    if FLAGS.servers and set(FLAGS.excludes).issuperset(FLAGS.servers):
        logging.fatal(
            '--excludes is a superset of --includes, no viable test server is '
            'possible. Ensure --excludes does not contain all --servers.')
    registry.register(
        SpeedtestCollector(servers=FLAGS.servers, excludes=FLAGS.excludes))
    metrics_handler = SpeedtestMetricsHandler.factory(registry)

    http = server.ThreadingHTTPServer((FLAGS.address, FLAGS.port),
                                      metrics_handler)

    logging.info('Starting HTTP server listening on %s:%s', FLAGS.address,
                 FLAGS.port)
    http.serve_forever()


def init():
    """Initializes the prometheus_speedtest cli."""
    app.run(main)


if __name__ == '__main__':
    init()
