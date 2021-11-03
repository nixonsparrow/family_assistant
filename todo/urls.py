from django.urls import path
from . import views


urlpatterns = [
    path('', views.TasksListView.as_view(), name='todo-all-tasks'),
    path('new', views.TaskCreateView.as_view(), name='todo-new-task'),
]
