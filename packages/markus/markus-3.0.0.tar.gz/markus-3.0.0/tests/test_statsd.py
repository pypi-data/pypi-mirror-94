# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from markus.backends import statsd
from markus.main import MetricsFilter, MetricsRecord


class MockStatsd:
    def __init__(self, *args, **kwargs):
        self.initargs = args
        self.initkwargs = kwargs
        self.calls = []

    def incr(self, *args, **kwargs):
        self.calls.append(("incr", args, kwargs))

    def gauge(self, *args, **kwargs):
        self.calls.append(("gauge", args, kwargs))

    def timing(self, *args, **kwargs):
        self.calls.append(("timing", args, kwargs))


@pytest.yield_fixture
def mockstatsd():
    """Mocks Statsd class to capture method call data"""
    _old_statsd = statsd.StatsClient
    mock = MockStatsd
    statsd.StatsClient = mock
    yield
    statsd.StatsClient = _old_statsd


def test_default_options(mockstatsd):
    ddm = statsd.StatsdMetrics()

    assert ddm.host == "localhost"
    assert ddm.port == 8125
    assert ddm.prefix is None
    assert ddm.maxudpsize == 512

    # NOTE: ddm.client is the mock instance
    assert ddm.client.initargs == ()
    assert ddm.client.initkwargs == {
        "host": "localhost",
        "port": 8125,
        "prefix": None,
        "maxudpsize": 512,
    }


def test_options(mockstatsd):
    ddm = statsd.StatsdMetrics(
        {
            "statsd_host": "example.com",
            "statsd_port": 5000,
            "statsd_prefix": "joe",
            "statsd_maxudpsize": 256,
        }
    )

    assert ddm.host == "example.com"
    assert ddm.port == 5000
    assert ddm.prefix == "joe"
    assert ddm.maxudpsize == 256

    # NOTE: ddm.client is the mock instance
    assert ddm.client.initargs == ()
    assert ddm.client.initkwargs == {
        "host": "example.com",
        "port": 5000,
        "prefix": "joe",
        "maxudpsize": 256,
    }


def test_incr(mockstatsd):
    rec = MetricsRecord("incr", key="foo", value=10, tags=["key1:val"])
    ddm = statsd.StatsdMetrics()
    ddm.emit_to_backend(rec)
    assert ddm.client.calls == [("incr", (), {"stat": "foo", "count": 10})]


def test_gauge(mockstatsd):
    rec = MetricsRecord("gauge", key="foo", value=100, tags=["key1:val"])
    ddm = statsd.StatsdMetrics()
    ddm.emit_to_backend(rec)
    assert ddm.client.calls == [("gauge", (), {"stat": "foo", "value": 100})]


def test_timing(mockstatsd):
    rec = MetricsRecord("timing", key="foo", value=1234, tags=["key1:val"])
    ddm = statsd.StatsdMetrics()
    ddm.emit_to_backend(rec)
    assert ddm.client.calls == [("timing", (), {"stat": "foo", "delta": 1234})]


def test_histogram(mockstatsd):
    rec = MetricsRecord("histogram", key="foo", value=4321, tags=["key1:val"])
    ddm = statsd.StatsdMetrics()
    ddm.emit_to_backend(rec)
    assert ddm.client.calls == [("timing", (), {"stat": "foo", "delta": 4321})]


def test_filters(mockstatsd):
    class BlueFilter(MetricsFilter):
        def filter(self, record):
            if "blue" not in record.key:
                return
            return record

    ddm = statsd.StatsdMetrics(filters=[BlueFilter()])
    ddm.emit_to_backend(MetricsRecord("incr", key="foo", value=1, tags=[]))
    ddm.emit_to_backend(MetricsRecord("incr", key="foo.blue", value=2, tags=[]))
    assert ddm.client.calls == [("incr", (), {"stat": "foo.blue", "count": 2})]
