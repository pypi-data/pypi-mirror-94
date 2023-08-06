# -*- coding: utf-8 -*-

import time

from pip_services3_components.count import CounterType, CachedCounters


class CountersFixture:

    __counters: CachedCounters

    def __init__(self, counters):
        self.__counters = counters

    def test_simple_counters(self):
        self.__counters.last("Test.LastValue", 123)
        self.__counters.last("Test.LastValue", 123456)

        counter = self.__counters.get("Test.LastValue", CounterType.LastValue)
        assert counter is not None
        assert counter.last is not None
        assert counter.last == 123456

        self.__counters.increment_one("Test.Increment")
        self.__counters.increment("Test.Increment", 3)

        counter = self.__counters.get("Test.Increment", CounterType.Increment)
        assert counter is not None
        assert counter.count == 4

        self.__counters.timestamp_now("Test.Timestamp")
        self.__counters.timestamp_now("Test.Timestamp")

        counter = self.__counters.get("Test.Timestamp", CounterType.Timestamp)
        assert counter is not None
        assert counter.time is not None

        self.__counters.stats("Test.Statistics", 1)
        self.__counters.stats("Test.Statistics", 2)
        self.__counters.stats("Test.Statistics", 3)

        counter = self.__counters.get("Test.Statistics", CounterType.Statistics)
        assert counter is not None
        assert counter.average == 2

        self.__counters.dump()

    def test_measure_elapsed_time(self):
        timer = self.__counters.begin_timing("Test.Elapsed")

        time.sleep(0.1)

        timer.end_timing()
        counter = self.__counters.get("Test.Elapsed", CounterType.Interval)
        assert counter.last > 50
        assert counter.last < 5000

        self.__counters.dump()
