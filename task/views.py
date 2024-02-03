from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import os
from .calculate_service import calculate_middle_value


@csrf_exempt
def post_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        task_id = calculate_middle_value(data)
        return JsonResponse({"message": "Data is being processed", "task_id": task_id}, status=202)
    
def get_data(request):
    if request.method == "GET":
        return JsonResponse({"message": "hello"}, status=200)
