from influxdb_client import InfluxDBClient as _InfluxDBClient, ApiClient
from influxdb_client.client.influxdb_client import _Configuration


class SSLClient(_InfluxDBClient):

    def __init__(self, url, token, ssl_ca_cert: str, debug=None, timeout=10000, enable_gzip=False, org: str = None,
                 default_tags: dict = None) -> None:
        super().__init__(url, token, debug, timeout, enable_gzip, org, default_tags)
        self.ssl_ca_cert = ssl_ca_cert
        self.url = url
        self.token = token
        self.timeout = timeout
        self.org = org

        self.default_tags = default_tags

        conf = _Configuration()
        if self.url.endswith("/"):
            conf.host = self.url[:-1]
        else:
            conf.host = self.url
        conf.enable_gzip = enable_gzip
        conf.debug = debug
        conf.verify_ssl = True
        conf.ssl_ca_cert = self.ssl_ca_cert

        auth_token = self.token
        auth_header_name = "Authorization"
        auth_header_value = "Token " + auth_token

        self.api_client = ApiClient(configuration=conf, header_name=auth_header_name,
                                    header_value=auth_header_value)
