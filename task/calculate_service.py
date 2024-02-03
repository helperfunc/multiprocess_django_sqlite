from .decorators import async_task
import json

@async_task
def calculate_middle_value(data):
    # 实现计算中位数的逻辑
    arr = data.get("data", [])
    sorted_data = sorted(arr)
    length = len(sorted_data)
    if length == 0:
        return 0
    if length % 2 == 0:
        return (sorted_data[length // 2 - 1] + sorted_data[length // 2]) / 2
    else:
        return sorted_data[length // 2]
