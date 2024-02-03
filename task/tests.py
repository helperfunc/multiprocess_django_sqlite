from django.test import TestCase
import requests
import json

url = 'http://localhost:8000/task/post-data/'
data = {"data": [1, 2, 3]}
url = 'http://localhost:8000/task/kill-process/'
data = {"task_ids": [54, 55]}


headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(data), headers=headers)

# 打印响应内容
print(response.status_code)
print(response.text)
