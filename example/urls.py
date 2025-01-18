# example/urls.py
from django.urls import path

from example.views import index, trigger_task_view, task_triggered_success_view


urlpatterns = [
    path('', index),
    path('trigger-task/', trigger_task_view),
    path('task-triggered-success/', task_triggered_success_view),
]