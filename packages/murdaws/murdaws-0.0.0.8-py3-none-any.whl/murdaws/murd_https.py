import json
from urllib3 import PoolManager

from .murd import MurdMap


_http = PoolManager()
_request = _http.request


class MurdHTTPClient:
    """ Murd API Client """

    def __init__(
        self,
        url
    ):
        self.url = url

    def update(
        self,
        mems,
        identifier="Unidentified"
    ):
        mems = MurdMap.prime_mems(mems)
        data = {'mems': json.dumps(mems)}
        resp = _request("PUT", self.url,
                        body=json.dumps(data).encode("utf-8"))

        if resp.status != 200:
            raise Exception("Murd update request failed")

    def read(
        self,
        row,
        col=None,
        greater_than_col=None,
        less_than_col=None
    ):
        data = {"row": row}
        if col is not None:
            data['col'] = col
        if greater_than_col is not None:
            data['greater_than_col'] = greater_than_col
        if less_than_col is not None:
            data['less_than_col'] = less_than_col
        resp = _request("POST", self.url,
                        body=json.dumps(data).encode("utf-8"))
        if resp.status != 200:
            raise Exception("Murd update request failed")

        read_data = json.loads(resp.data.decode("utf-8"))
        read_data = [MurdMap(**rd) for rd in read_data]
        return read_data

    def delete(self, mems):
        mems = MurdMap.prime_mems(mems)
        data = {'mems': json.dumps(mems)}
        resp = _request("DELETE", self.url,
                        body=json.dumps(data).encode('utf-8'))

        if resp.status != 200:
            raise Exception("Murd delete request failed")

        stubborn_mems = json.loads(resp.data.decode("utf-8"))
        return [MurdMap(**sm) for sm in stubborn_mems]
