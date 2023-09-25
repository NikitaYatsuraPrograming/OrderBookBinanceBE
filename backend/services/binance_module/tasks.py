import json
from json import JSONDecodeError

from celery import shared_task
from sqlalchemy import select, insert

from db.connect_db import sync_engine
from db.connection_redis import connect_redis_sync
from services.binance_module.models import BinanceHistoryLastKeyRedis, Binance


@shared_task()
def save_data_with_redis_in_db_task():
     with sync_engine.begin() as session:
        query = session.execute(select(BinanceHistoryLastKeyRedis).order_by(BinanceHistoryLastKeyRedis.id.desc()))
        last_history_obj  = query.first()
        redis_keys = connect_redis_sync.keys()
        if bytes(last_history_obj.key, 'utf-8') in redis_keys:
            # TODO сохранить первую запись в редис в бд
            position = redis_keys.index(bytes(last_history_obj.key, 'utf-8')) + 1
        else:
            position = 0
        if redis_keys:
            stmt = insert(BinanceHistoryLastKeyRedis).values(key=str(redis_keys[-1].decode('utf-8')))
            stmt.compile()

        data_save = []
        for key in redis_keys[position::]:
            value_bytes = connect_redis_sync.get(key)
            try:
                value = json.loads(value_bytes.decode('utf-8'))
            except JSONDecodeError:
                continue
            data_save.append(value)

        if data_save:
            session.execute(insert(Binance), data_save)
            session.commit()

        