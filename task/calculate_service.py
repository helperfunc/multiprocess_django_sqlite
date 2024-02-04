from .decorators import async_task
import ray
import json
from .models import Task, TaskStatus


#@async_task
@ray.remote
def calculate_middle_value(data, task_id):
    # 实现计算中位数的逻辑
    import django
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multiprocess_django_sqlite.settings')
    django.setup()
    import time
    from .models import Task, TaskStatus
    task = Task.objects.get(id=task_id)
    try:
        time.sleep(20)
        arr = data.get("data", [])
        sorted_data = sorted(arr)
        length = len(sorted_data)
        task.status = TaskStatus.Completed.value
        res = 0
        if length == 0:
            res = 0
        if length % 2 == 0:
            res = (sorted_data[length // 2 - 1] + sorted_data[length // 2]) / 2
        else:
            res = sorted_data[length // 2]
        task.result = str(res)
        return res
    except Exception as e:
        task.result = str(e)
        task.status = TaskStatus.Failed.value
    finally:
        task.save()


def update_task_status_killed(data):
    arr = data.get('task_ids', [])
    tasks = Task.objects.filter(id__in=arr)
    for task in tasks:
        task.status = TaskStatus.Kill.value
    
    Task.objects.bulk_update(tasks, ["status"])


def save_new_task(futures, data):
    input_data = json.dumps(data) if data else '{}'
    task = Task.objects.create(
        function_path=f'{futures.__module__}.{futures._function_name}',
        input_data=input_data
    )
    return task.id  # 创建新任务并返回任务 ID