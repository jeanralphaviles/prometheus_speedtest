"""Tests prometheus_speedtest.py."""

import collections
import multiprocessing
import unittest

import mock
import speedtest

import prometheus_speedtest


class PrometheusSpeedtestTest(unittest.TestCase):
  """Tests prometheus_speedtest.PrometheusSpeedtest."""

  _results = collections.namedtuple('Results', ['download', 'upload', 'ping'])

  @mock.patch.object(multiprocessing, 'Pool')
  @mock.patch.object(speedtest, 'Speedtest', autospec=True)
  def test_test(self, mock_speedtest, mock_pool):
    tester = prometheus_speedtest.PrometheusSpeedtest(source_address='4.3.2.1')


    expected = PrometheusSpeedtestTest._results(10, 5, 30)
    mock_pool.return_value.apply_async.return_value.get.return_value = (
        prometheus_speedtest._perform_test('4.3.2.1'))
    mock_speedtest.return_value.results = expected

    self.assertEqual(tester._test(), expected)

    mock_speedtest.assert_called_once_with(source_address='4.3.2.1')
    mock_speedtest.return_value.get_best_server.assert_called_once_with()
    mock_speedtest.return_value.download.assert_called_once_with()
    mock_speedtest.return_value.upload.assert_called_once_with()

  @mock.patch.object(multiprocessing, 'Pool')
  def test_testTimeout(self, mock_pool):
    tester = prometheus_speedtest.PrometheusSpeedtest(None, timeout=1)

    mock_async_result = mock.MagicMock()
    mock_pool.return_value.apply_async.return_value = mock_async_result
    mock_async_result.get.side_effect = multiprocessing.TimeoutError

    self.assertRaises(prometheus_speedtest.TimeoutError, tester._test)
    mock_async_result.get.assert_called_with(1)

  @mock.patch.object(prometheus_speedtest.PrometheusSpeedtest, '_metrics')
  @mock.patch.object(prometheus_speedtest.PrometheusSpeedtest, '_test')
  def test_report(self, mock_test, mock_metrics):
    tester = prometheus_speedtest.PrometheusSpeedtest()
    results = PrometheusSpeedtestTest._results(10, 5, 30)

    mock_test.return_value = results

    tester.report()

    mock_metrics.assert_called_once_with(results)


if __name__ == '__main__':
  unittest.main()
