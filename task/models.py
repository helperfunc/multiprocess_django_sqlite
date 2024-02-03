from django.db import models
from enum import Enum

class TaskStatus(Enum):
    Processing = 'processing'
    Processed = 'processed'
    Failed = 'failed'
    Completed = 'completed'
    Kill = 'kill'
    Killed = 'Killed'

class Task(models.Model):
    function_path = models.CharField(max_length=255)
    input_data = models.TextField()
    result = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, default=TaskStatus.Processing.value)

