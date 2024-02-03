from django.db import models

class Task(models.Model):
    function_path = models.CharField(max_length=255)
    input_data = models.TextField()
    result = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, default='processing')
