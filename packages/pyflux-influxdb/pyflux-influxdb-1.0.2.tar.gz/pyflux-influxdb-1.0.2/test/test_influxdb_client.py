import os
from unittest import TestCase

from pyflux_influxdb.influxdb_client import SSLClient


class InfluxdbClientTestCase(TestCase):

    def setUp(self) -> None:
        self.base_dir = os.path.dirname(__file__)
        self.ssl_ca_cert = os.path.join(self.base_dir, 'ca.crt')

    def test_query(self):
        c = SSLClient(
            url='https://192.168.254.75:8086', token='admin:zaq1<LP_', org='-',
            ssl_ca_cert=self.ssl_ca_cert
        )
        query_api = c.query_api()

        result = query_api.query("""
        from(bucket: "oplatform/autogen")
        |> range(start:-2h)
        |> filter(fn: (r) =>
              r._measurement == "if.info" and 
              r._field == "duplex"
           )
        """, org='-')

        for res in result:
            for col in res.columns:
                print(col.label)

            for rec in res.records:
                print(rec)