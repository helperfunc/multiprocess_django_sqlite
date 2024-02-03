import os
from functools import wraps
from .models import Task
import json

def async_task(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 检查环境变量
        if os.getenv('CREATE_TASK', 'True') == 'True':
            input_data = json.dumps(args[0:]) if args else '{}'
            task = Task.objects.create(
                function_path=f'{func.__module__}.{func.__name__}',
                input_data=input_data
            )
            return task.id  # 创建新任务并返回任务 ID
        else:
            # 直接执行原函数，不创建新任务
            return func(*args, **kwargs)
    return wrapper
