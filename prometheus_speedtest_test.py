#!/usr/bin/python3
"""Tests prometheus_speedtest.py."""

import collections
import unittest

import mock
import prometheus_client
import speedtest

import prometheus_speedtest


class PrometheusSpeedtestTest(unittest.TestCase):
    """Tests prometheus_speedtest.PrometheusSpeedtest."""

    _results = collections.namedtuple('Results',
                                      ['download', 'upload', 'ping'])

    @mock.patch.object(speedtest, 'Speedtest', autospec=True)
    def test_test(self, mock_speedtest):
        """Ensures correctness of PrometheusSpeedtest.test()."""
        tester = prometheus_speedtest.PrometheusSpeedtest(
            source_address='4.3.2.1', timeout=10)

        expected = PrometheusSpeedtestTest._results(10, 5, 30)
        mock_speedtest.return_value.results = expected

        self.assertEqual(tester.test(), expected)

        mock_speedtest.assert_called_once_with(
            source_address='4.3.2.1', timeout=10)
        mock_speedtest.return_value.get_best_server.assert_called_once_with()
        mock_speedtest.return_value.download.assert_called_once_with()
        mock_speedtest.return_value.upload.assert_called_once_with()


class SpeedtestCollectorTest(unittest.TestCase):
    """Tests prometheus_speedtest.SpeedtestCollector."""

    _results = collections.namedtuple(
        'Results',
        ['download', 'upload', 'ping', 'bytes_received', 'bytes_sent'])

    @staticmethod
    @mock.patch.object(prometheus_client.core.GaugeMetricFamily, 'add_metric')
    def test_collect(mock_metric):
        """Ensures correctness of SpeedtestCollector.collect()."""
        mock_tester = mock.create_autospec(
            prometheus_speedtest.PrometheusSpeedtest)
        collector = prometheus_speedtest.SpeedtestCollector(mock_tester)

        speedtest_results = [10, 5, 30, 100, 20]
        mock_tester.test.return_value = SpeedtestCollectorTest._results(
            *speedtest_results)

        collections.deque(collector.collect())

        mock_metric.assert_has_calls(
            [mock.call(
                labels=[], value=value) for value in speedtest_results])


if __name__ == '__main__':
    unittest.main()
