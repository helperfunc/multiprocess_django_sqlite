from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .calculate_service import calculate_middle_value, update_task_status_killed, save_new_task


@csrf_exempt
def post_data(request): #localhost:8000/task/post-data/  {"data": [1,2,3]}
    if request.method == "POST":
        data = json.loads(request.body)
        # task_id = calculate_middle_value(data)
        task_id = save_new_task(calculate_middle_value, data)
        futures = calculate_middle_value.remote(data, task_id)
        return JsonResponse({"message": "Data is being processed", "task_id": task_id}, status=202)
    

def get_data(request):  #localhost:8000/task/get-data/
    if request.method == "GET":
        return JsonResponse({"message": "hello"}, status=200)


@csrf_exempt
def kill_process(request):  # localhost:8000/task/kill-process/  {"task_ids": [1,2,3]}
    if request.method == "POST":
        data = json.loads(request.body)
        update_task_status_killed(data)
        return JsonResponse({"message": "tasks are killed"}, status=200)