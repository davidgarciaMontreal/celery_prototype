import time
from math import sqrt
from celery import Celery


class Data:
    def __init__(self):
        self.time = time.time()

    def __str__(self):
        return f'a{self.time}a'
    def get_time(self):
        return self.time

local = '127.0.0.1'
port = 6379
url = f'redis://{local}:{port}/0'
app = Celery('tasks', broker=url)
config = {'CELERY_RESULT_BACKEND': url,
          'CELERY_ACCEPT_CONTENT': ['pickle', 'json'],
          'CELERY_TASK_SERIALIZER': ['pickle', 'json'],
          'CELERY_RESULT_SERIALIZER': 'pickle'
          }

app.conf.update(config)


@app.task
def square_root(value):
    time.sleep(5)
    return sqrt(value)


@app.task(serializer='pickle')
def data():
    time.sleep(5)
    return Data()

