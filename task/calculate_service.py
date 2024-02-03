from .decorators import async_task
from .models import Task, TaskStatus
import time

@async_task
def calculate_middle_value(data):
    # 实现计算中位数的逻辑
    time.sleep(20)
    arr = data.get("data", [])
    sorted_data = sorted(arr)
    length = len(sorted_data)
    if length == 0:
        return 0
    if length % 2 == 0:
        return (sorted_data[length // 2 - 1] + sorted_data[length // 2]) / 2
    else:
        return sorted_data[length // 2]


def update_task_status_killed(data):
    arr = data.get('task_ids', [])
    tasks = Task.objects.filter(id__in=arr)
    for task in tasks:
        task.status = TaskStatus.Kill.value
    
    Task.objects.bulk_update(tasks, ["status"])