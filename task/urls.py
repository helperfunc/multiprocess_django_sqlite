from django.urls import path
from . import views

urlpatterns = [
    # 其他 URL 模式...
    path('post-data/', views.post_data, name='post_data'),
    path('get-data/', views.get_data, name='get_data'),
    path('kill-process/', views.kill_process, name='kill_process')
]
