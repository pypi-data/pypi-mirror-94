import os
from unittest import TestCase

from pyflux_influxdb.flux import *
from pyflux_influxdb.influxdb_client import SSLClient
from pyflux_influxdb.type_convert import uint


class FluxTestCase(TestCase):
    def setUp(self) -> None:
        self.base_dir = os.path.dirname(__file__)
        self.ssl_ca_cert = os.path.join(self.base_dir, 'ca.crt')
        self.client = SSLClient(
            url='https://192.168.254.75:8086', token='admin:zaq1<LP_', org='-',
            ssl_ca_cert=self.ssl_ca_cert
        )
        self.time_start = '-5h'
        self.fluxR = FluxR()

    def query(self, script):
        q = self.client.query_api()
        res = q.query(script)
        print(res)
        return res

    def test_filter(self):
        flux_query = FluxQuery(bucket='oplatform/autogen')
        res = flux_query.range(self.time_start).filter(
            FluxQ(self.fluxR._measurement, 'if.info') &
            FluxQ(self.fluxR._filed, 'duplex')
        )
        self.query(res.get_script())

    def test_pivot(self):
        flux_query = FluxQuery(bucket='oplatform/autogen')
        res = flux_query.range(self.time_start).filter(
            FluxQ(self.fluxR._measurement, 'if.info')
        ).pivot(
            ['_time'],
            ['_field', 'device_id'],
            '_value'
        )
        self.query(res.get_script())

    def test_limit(self):
        flux_query = FluxQuery(bucket='oplatform/autogen')
        res = flux_query.range(self.time_start).pivot(['_time'], ['_field'], '_value').limit(1)
        for r in self.query(res.get_script()):
            self.assertLessEqual(len(r.records), 1)

    def test_duplicate(self):
        flux_query = FluxQuery(bucket='oplatform/autogen')
        res = flux_query.range(self.time_start).pivot(['_time'], ['_field'], '_value').limit(1).duplicate('_time',
                                                                                                          'collect_time')
        self.query(res.get_script())

    def test_sort(self):
        flux_query = FluxQuery(bucket='oplatform/autogen')
        res = flux_query.range(self.time_start).pivot(
            ['_time'],
            ['_field'],
            '_value').limit(1).sort(['_time'])
        self.query(res.get_script())

    def test_count(self):
        flux_query = FluxQuery(bucket='oplatform/autogen')
        res = flux_query.range(self.time_start).filter(FluxQ(self.fluxR._measurement, 'if.info')).pivot(
            ['_time'],
            ['_field'],
            '_value').count('interface')
        self.query(res.get_script())

    def test_first(self):
        flux_query = FluxQuery(bucket='oplatform/autogen')
        res = flux_query.range(self.time_start).filter(FluxQ(self.fluxR._measurement, 'if.info')).first().pivot(
            ['_time'],
            ['_field'],
            '_value')
        self.query(res.get_script())

    def test_last(self):
        flux_query = FluxQuery(bucket='oplatform/autogen')
        res = flux_query.range(self.time_start).filter(FluxQ(self.fluxR._measurement, 'if.info')).last().pivot(
            ['_time'],
            ['_field'],
            '_value')
        self.query(res.get_script())

    def test_map(self):
        flux_query = FluxQuery(bucket='oplatform/autogen')
        res = flux_query.range(self.time_start).filter(FluxQ(self.fluxR._measurement, 'if.info')).map({
            '_time': uint(self.fluxR._time)
        })
        self.query(res.get_script())

    def test_group(self):
        flux_query = FluxQuery(bucket='oplatform/autogen')
        res = flux_query.range(self.time_start).filter(FluxQ(self.fluxR._measurement, 'if.info')).pivot(
            ['_time'],
            ['_field'],
            '_value').group(group_columns=["_measurement"]).sort()
        self.query(res.get_script())

    def test_drop(self):
        flux_query = FluxQuery(bucket='oplatform/autogen')
        res = flux_query.range(self.time_start).filter(
            FluxQ(self.fluxR._measurement, 'if.info')
        ).pivot(
            ['_time'],
            ['_field', 'device_id'],
            '_value'
        ).drop(['_measurement'])
        self.query(res.get_script())

    def test_rename(self):
        flux_query = FluxQuery(bucket='oplatform/autogen')
        res = flux_query.range(self.time_start).filter(
            FluxQ(self.fluxR._measurement, 'if.info')
        ).pivot(
            ['_time'],
            ['_field', 'device_id'],
            '_value'
        ).rename({'_time': 'time'})
        data = self.query(res.get_script())
        print(data)
