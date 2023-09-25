from celery import Celery
from celery.schedules import crontab
import os
from services.binance_module import tasks

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/10'
CELERY_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}'
BROKER_TRANSPORT = 'redis'
CELERY_SEND_TASK_SENT_EVENT = True
CELERY_IMPORTS = ('services.binance_module',)

app = Celery('order_book_binance')
app.conf.broker_url = CELERY_BROKER_URL
app.conf.result_backend = CELERY_BACKEND
app.autodiscover_tasks(['services.binance_module'])

app.conf.timezone = 'UTC'

app.conf.beat_schedule = {
    'start_every_1_hour_save_data_with_redis_in_db_task': {
            'task': 'services.binance_module.tasks.save_data_with_redis_in_db_task',
            'schedule': crontab(hour='*/1')
        },
}
