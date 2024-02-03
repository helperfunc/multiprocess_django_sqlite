import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multiprocess_django_sqlite.settings')
django.setup()

import time
from task.models import Task, TaskStatus
import importlib
import json
import multiprocessing
import psutil

os.environ['CREATE_TASK'] = 'False'


def execute_task(task_id, task_queue):
    task = Task.objects.get(id=task_id)

    try:
        module_name, function_name = task.function_path.rsplit('.', 1)
        module = importlib.import_module(module_name)
        func = getattr(module, function_name)

        data = json.loads(task.input_data)
        result = func(*data)  # 假设函数接受解包的参数列表

        task.result = json.dumps(result)
        task.status = TaskStatus.Completed.value
    except Exception as e:
        task.result = str(e)
        task.status = TaskStatus.Failed.value
    finally:
        task.save()

        task.refresh_from_db()
        if task.status == TaskStatus.Kill.value:
            task_queue.put((TaskStatus.Kill.value, task_id))


def worker(task_queue, task_to_process):
    current_task_id = None

    while True:
        task_info = task_queue.get()
        if task_info is None:
            break

        if isinstance(task_info, tuple) and task_info[0] == TaskStatus.Kill.value:
            if task_info[1] == current_task_id:
                break
            continue

        if isinstance(task_info, int):
            current_task_id = task_info
            task_to_process[current_task_id] = multiprocessing.current_process().pid
            print('task id %d, PID %d' % (current_task_id, task_to_process[current_task_id]))
            execute_task(current_task_id, task_queue)
            del task_to_process[current_task_id]


def kill_process_and_children(pid, task):
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        child.kill()
    parent.kill()
    task.status = TaskStatus.Killed.value
    task.save()
    print('PID %d is killed' % pid)


def manage_workers():
    with multiprocessing.Manager() as manager:
        task_queue = multiprocessing.Queue()
        task_to_process = manager.dict()
        workers = []

        for _ in range(4):
            p = multiprocessing.Process(target=worker, args=(task_queue, task_to_process))
            p.start()
            workers.append(p)

        while True:
            number_tasks = task_queue.qsize()
            
            # 遍历数据库中的任务，筛选出需要添加到队列的任务
            for task in Task.objects.filter(status=TaskStatus.Processing.value):
                task_queue.put(task.id)
                task.status = TaskStatus.Processed.value
                task.save()

            if task_queue.qsize() != number_tasks:
                print('task engine running, added %d tasks to the task engine' % (task_queue.qsize() - number_tasks))
            else:
                print('task engine running') 
            
            for task_id in list(task_to_process.keys()):
                task = Task.objects.get(id=task_id)
                if task.status == TaskStatus.Kill.value:
                    pid = task_to_process[task_id]
                    kill_process_and_children(pid, task)
                    del task_to_process[task_id]

            for i in range(len(workers)):
                if not workers[i].is_alive():
                    workers[i].join()
                    new_worker = multiprocessing.Process(target=worker, args=(task_queue, task_to_process))
                    new_worker.start()
                    workers[i] = new_worker
                    print('new worker started')

            time.sleep(5)


if __name__ == '__main__':
    # Windows系统需要freeze_support()
    multiprocessing.freeze_support()

    # 启动进程管理
    manage_workers()