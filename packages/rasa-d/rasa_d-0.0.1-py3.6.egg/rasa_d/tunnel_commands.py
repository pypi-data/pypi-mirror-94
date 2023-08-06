import ssl
import json
import base64
import asyncio
import logging
import aiohttp
import certifi
import websockets
import webbrowser
from urllib.parse import urljoin


logger = logging.getLogger("rasa-d.client")


class Client:
    def __init__(self, base_uri, token):
        self.base_uri = base_uri
        self.token = token

    async def process(self, message, websocket):
        async with aiohttp.ClientSession() as session:
            try:
                response = await session.request(
                    method="POST",
                    url=urljoin(self.base_uri, message['url']),
                    headers=message['header'],
                    data=base64.b64decode(message['body']),
                )
            except:
                print(f"Error Processing Request At: {message['url']}")
                return {
                    'request_id': message['id'],
                    'token': self.token,
                    'status': 500,
                    'header': {},
                    'body': base64.b64encode(b'request failed').decode('utf-8'),
                }

            print(message["method"], message["url"], response.status)
            body = await response.read()
            response_message = {
                'request_id': message['id'],
                'token': self.token,
                'status': response.status,
                'header': dict(response.headers),
                'body': base64.b64encode(body).decode('utf-8'),
            }
            await websocket.send(json.dumps(response_message))



async def open_tunnel(ws_uri: str, http_uri):
    ssl_context = ssl.create_default_context()
    ssl_context.load_verify_locations(certifi.where())
    async with websockets.connect(ws_uri, ssl=ssl_context) as websocket:
        message = json.loads(await websocket.recv())
        host, token = message["host"], message["token"]
        logger.info(f"Online at https://{host}/")
        webbrowser.open(f'https://{host}/', new=2)

        client = Client(http_uri, token)
        while True:
            message = json.loads(await websocket.recv())
            asyncio.ensure_future(client.process(message, websocket))