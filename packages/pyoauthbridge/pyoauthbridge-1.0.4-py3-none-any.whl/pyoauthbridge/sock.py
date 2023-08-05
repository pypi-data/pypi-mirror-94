import asyncio
import websockets
import logging
import json
from io import BytesIO
from bytes_marketdata import CliMarketdataRes
from bytes_marketdata import GetModePacket
from map_message import market_data

class WebSocket:
    def __init__(self, base_url):
        self.base_url = base_url
        self.socket = ""

    async def connect(self):
        base_url = self.base_url
        async with websockets.connect(base_url) as websocket:
            self.socket = websocket
            print("print")

    def start_socket(self):
        asyncio.get_event_loop().run_until_complete(self.connect())
        asyncio.get_event_loop().run_forever()

    async def subscribe(self, payload, message_type):
        message = {"a": "subscribe"}
        if(message_type == "marketdata"):
            message['v'] = [[payload.exchange_code, payload.token]]
            message['m'] = "marketdata"
        await websocket.send(json.dumps(message))

    async def get_market_data(self, token, exchange_code, _callback = None):
            marketdataPkt = CliMarketdataRes()
            mode_data_pkt = GetModePacket()
            print(token)
            async for message in websocket:
                if(mode_data_pkt.get_mode(message)==1):
                    marketdataPkt.get_CliMarketdataRes_Instruct(message)
                    if(marketdataPkt.exchange_code == exchange_code and marketdataPkt.instrument_token == token):
                        market_data_feeds = market_data(marketdataPkt)
                        _callback(market_data_feeds)

def handler(data):
    print(data)
if __name__ == "__main__":
    websocket = WebSocket("wss://mimik.tradelab.in/ws/v1/feeds?login_id=SATYAM&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJibGFja2xpc3Rfa2V5IjoiU0FUWUFNOlZlUHJFeGV2dXlxMHNicWMvWlZqbGciLCJjbGllbnRfaWQiOiJTQVRZQU0iLCJjbGllbnRfdG9rZW4iOiJVcnVHSEJjRFhYUG52R0ZOVkhhZ3ZRIiwiZGV2aWNlIjoid2ViIiwiZXhwIjoxNjEyNTk3MzA1Nzk4fQ.L5h7iXN6qBG3fJ99bsHZ5lrLG6CVL1paCPMmisFyNJc")
    websocket.start_socket()
    payload = {
        "exchange_code": 1,
        "token": 3045,
    }
    websocket.subscribe(payload, "marketdata")
    websocket.get_market_data(3045, 1, handler)