import aioredis
import uvicorn
from fastapi import FastAPI, WebSocket

from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect

from services.binance_module.tasks import save_data_with_redis_in_db_task
from settings.redis_setting import REDIS_PORT, REDIS_HOST

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    from services.connection.connection import manager, binance_manager
    save_data_with_redis_in_db_task()
    await manager.connect(websocket)
    if binance_manager.active_connections is None:
        await binance_manager.connect()
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.on_event('startup')
async def register_redis():
    app.state.redis = await aioredis.from_url(
        f'redis://{REDIS_HOST}',
        port=REDIS_PORT,
        db=5,
        encoding='utf-8'
    )


@app.on_event('startup')
async def create_unique_key_for_redis_and_db_history():
    from services.connection.connection import default_code_generator
    app.state.unique_key_dict = {'unique_key': await default_code_generator(), 'is_use': False }


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8082, reload=True)



