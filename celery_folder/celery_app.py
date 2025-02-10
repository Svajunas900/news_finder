from celery import Celery
from datetime import timedelta


app = Celery("celery_app", broker='redis://redis:6379/0', backend='redis://redis:6379/0', include=["tasks"])
app.conf.beat_schedule = {
    'my-periodic-task': {
        'task': 'tasks.compare_headlines',
        'schedule': timedelta(seconds=30), 
    },
}