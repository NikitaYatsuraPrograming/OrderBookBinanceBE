import random
import string
from abc import ABCMeta, abstractmethod

import websockets
from fastapi import WebSocket

from starlette.websockets import WebSocketDisconnect

from db.connect_db import async_session
from main import app
from services.binance_module.models import BinanceHistoryLastKeyRedis


async def default_code_generator(size=32):
    choices = [*string.digits, *string.ascii_uppercase, *string.ascii_lowercase]
    unique_key = ''.join([random.choice(choices) for _ in range(size)])

    if await app.state.redis.get(unique_key) is not None:
        unique_key = default_code_generator()

    return unique_key


class Connection(metaclass=ABCMeta):

    @abstractmethod
    async def connect(self, *args, **kwargs):
        pass

    @abstractmethod
    def disconnect(self, *args, **kwargs):
        pass

    @abstractmethod
    async def broadcast(self, message):
        pass

class ConnectionManager(Connection):
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message):
        for connection in self.active_connections:
            try:
                await connection.send_text(str(message))
            except WebSocketDisconnect:
                manager.disconnect(connection)


class ConnectionBinanceManager(Connection):
    def __init__(self):
        self.active_connections = None

    async def set_data_in_redis(self, message):
        if not app.state.unique_key_dict['is_use']:
            unique_key = app.state.unique_key_dict['unique_key']
            history = BinanceHistoryLastKeyRedis(key=unique_key)
            async with async_session() as session:
                session.add(history)
                await session.commit()
            app.state.unique_key_dict['is_use'] = True
        else:
            unique_key = await default_code_generator()
        await app.state.redis.set(unique_key, message)

    async def message(self,  websocket):
        self.active_connections = websocket
        while True:
            try:
                async for message in websocket:
                    await self.set_data_in_redis(message=message)
                    await self.broadcast(message=message)
            except websockets.ConnectionClosed:
                self.disconnect()
                break

    async def broadcast(self, message):
        await manager.broadcast(message)

    async def connect(self):
        async with websockets.connect('wss://stream.binance.com:443/ws/ethbtc@depth') as websocket:
            await self.message(websocket)

    def disconnect(self):
        self.active_connections = None


manager = ConnectionManager()
binance_manager = ConnectionBinanceManager()