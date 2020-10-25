import logging
import time
import threading
import multiprocessing
import argparse
class Data:
    def __init__(self):
        self.time = time.ctime()
    def __str__(self):
        return f'{self.time}'

from celery import Celery
def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
logging.basicConfig(level=logging.DEBUG)
local = '127.0.0.1'
port = 6379
url = f'redis://{local}:{port}/0'
app = Celery('tasks', broker=url)
config = {'CELERY_RESULT_BACKEND': url,
          'CELERY_ACCEPT_CONTENT': ['pickle', 'json'],
          'CELERY_RESULT_SERIALIZER': 'pickle'
          }
app.conf.update(config)


def manage_sqrt_task(value):
    result = app.send_task('tasks.square_root', args=(value,))
    logging.info(result.get())

def manage_data(b: threading.Barrier):
    b.wait()
    t = time.time()
    result = app.send_task('tasks.data', args=())
    data = result.get()
    delta = data.get_time() - t
    logging.info(f'The Overall time taken is {delta}')

def count_down(cnt:int, b: threading.Barrier):
    b.wait()
    t = time.time()
    while cnt > 0:
        cnt -=1
    delta = time.time() - t
    print(f"time taken {delta}")

def count_down_m(cnt:int, b: multiprocessing.Barrier):
    b.wait()
    print(f'Starting {time.ctime()}')
    t = time.time()
    while cnt > 0:
        cnt -= 1
    delta = time.time() - t
    print(f"time taken {delta}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--parallel", type=str2bool, required=True, help="increase output verbosity")
    parser.add_argument("--number", type=int, required=True, help="increase output verbosity")
    args = parser.parse_args()
    n = args.number
    cnt = 500_000_000
    tasks = list()

    if not args.parallel:
        print('running in threaded mode')
        b = threading.Barrier(n)
        for i in range(n):
            t = threading.Thread(target=manage_data, args=(b,))
            tasks.append(t)
    else:
        print('running in parallel mode')
        b = multiprocessing.Barrier(n)
        for i in range(n):
            t = multiprocessing.Process(target=count_down_m, args=(cnt,b,))
            tasks.append(t)

    for t in tasks:
        t.start()
    for t in tasks:
        t.join()
