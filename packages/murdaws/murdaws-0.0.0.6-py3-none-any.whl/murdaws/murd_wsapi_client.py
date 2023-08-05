import json
from websocket import create_connection
from murd import MurdMap


class MurdWSClient:
    """ Murd WebSocket API Client """

    def __init__(
        self,
        url
    ):
        self.url = url
        self.ws = create_connection(self.url)

    @staticmethod
    def prime_mems(mems):
        return list({(MurdMap(**ob)['ROW'], MurdMap(**ob)['COL']): ob for ob in mems}.values())

    def update(
        self,
        mems,
        identifier="Unidentified"
    ):
        mems = self.prime_mems(mems)
        update_request = {'mems': json.dumps(mems), 'route': 'update'}
        self.ws.send(json.dumps(update_request))

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
        read_request = {'route': 'read', 'request': json.dumps(data)}
        self.ws.send(json.dumps(read_request))

        # Listen for read response
        read_data = self.ws.recv()
        read_data = json.loads(read_data)
        read_data = [MurdMap(**rd) for rd in read_data]
        return read_data

    def delete(self, mems):
        mems = self.prime_mems(mems)
        delete_request = {'mems': json.dumps(mems), 'route': 'delete'}
        self.ws.send(json.dumps(delete_request))

        stubborn_mems = self.ws.recv()
        stubborn_mems = json.loads(stubborn_mems)
        return [MurdMap(**sm) for sm in stubborn_mems]
