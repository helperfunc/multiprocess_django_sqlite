import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multiprocess_django_sqlite.settings')
django.setup()

import time
from task.models import Task
import importlib
import json
from multiprocessing import Process

os.environ['CREATE_TASK'] = 'False'


def process_task():
    tasks = Task.objects.filter(status='processing')
    for task in tasks:
        try:
            module_name, function_name = task.function_path.rsplit('.', 1)
            module = importlib.import_module(module_name)
            func = getattr(module, function_name)
            data = json.loads(task.input_data)
            result = func(*data)
            task.result = json.dumps(result)
            task.status = 'completed'
        except Exception as e:
            task.result = str(e)
            task.status = 'failed'
        task.save()


def run_worker():
    while True:
        process_task()
        time.sleep(5)  # 间隔一段时间再次检查任务


run_worker()