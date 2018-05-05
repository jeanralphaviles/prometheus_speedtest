"""Tests prometheus_speedtest.py."""

import collections
import socket
import threading
import unittest

import mock
import prometheus_client
import speedtest

import prometheus_speedtest


class PrometheusSpeedtestTest(unittest.TestCase):
  """Tests prometheus_speedtest.PrometheusSpeedtest."""

  _results = collections.namedtuple('Results', ['download', 'upload', 'ping'])

  @mock.patch.object(speedtest, 'Speedtest', autospec=True)
  def test_test(self, mock_speedtest):
    tester = prometheus_speedtest.PrometheusSpeedtest(
        None, None, source_address='4.3.2.1')

    expected = PrometheusSpeedtestTest._results(10, 5, 30)
    mock_speedtest.return_value.results = expected

    self.assertEqual(tester._test(), expected)

    mock_speedtest.assert_called_once_with(source_address='4.3.2.1')
    mock_speedtest.return_value.get_best_server.assert_called_once_with()
    mock_speedtest.return_value.download.assert_called_once_with()
    mock_speedtest.return_value.upload.assert_called_once_with()

  @mock.patch.object(threading, 'Thread')
  def test_testTimeout(self, mock_thread):
    tester = prometheus_speedtest.PrometheusSpeedtest(None, None, timeout=1)

    mock_thread.return_value.is_alive.return_value = True

    self.assertRaises(prometheus_speedtest.TimeoutError, tester._test)

    mock_thread.return_value.join.assert_called_once_with(1)


  @mock.patch.object(socket, 'gethostname')
  @mock.patch.object(prometheus_client, 'Gauge')
  @mock.patch.object(prometheus_client, 'push_to_gateway')
  def test_push(self, mock_push_to_gateway, mock_gauge, mock_gethostname):
    tester = prometheus_speedtest.PrometheusSpeedtest('1.2.3.4:1234', 'test')
    results = PrometheusSpeedtestTest._results(10, 5, 30)

    mock_download = mock.MagicMock()
    mock_upload = mock.MagicMock()
    mock_ping = mock.MagicMock()
    mock_gauge.side_effect = (mock_download, mock_upload, mock_ping)
    mock_gethostname.return_value = 'testhost'

    tester._push(results)

    mock_download.set.assert_called_once_with(10)
    mock_upload.set.assert_called_once_with(5)
    mock_ping.set.assert_called_once_with(30)

    mock_push_to_gateway.assert_called_once_with(
        '1.2.3.4:1234', job='test', grouping_key={'instance': 'testhost'},
        registry=mock.ANY)

  @mock.patch.object(prometheus_speedtest.PrometheusSpeedtest, '_push')
  @mock.patch.object(prometheus_speedtest.PrometheusSpeedtest, '_test')
  def test_report(self, mock_test, mock_push):
    tester = prometheus_speedtest.PrometheusSpeedtest(None, None)
    results = PrometheusSpeedtestTest._results(10, 5, 30)

    mock_test.return_value = results

    tester.report()

    mock_push.assert_called_once_with(results)


if __name__ == '__main__':
  unittest.main()
