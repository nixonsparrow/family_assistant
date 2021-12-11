from django.urls import path
from . import views


# do not create path with empty string here - ""
urlpatterns = [
    path('tasks', views.TasksListView.as_view(), name='todo-all-tasks'),
    path('new-task', views.TaskCreateView.as_view(), name='todo-new-task'),
    path('tasks/<int:pk>', views.TaskUpdateView.as_view(), name='todo-task-update'),
]
