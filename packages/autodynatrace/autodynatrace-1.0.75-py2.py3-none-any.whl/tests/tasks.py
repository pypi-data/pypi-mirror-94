import random
import time

from celery import Celery

import autodynatrace

app = Celery("tasks", broker="pyamqp://guest@localhost//")


@app.task
def add(x, y):
    print("Adding {}, {}".format(x, y))
    time.sleep(random.randint(1, 3))
    return x + y
