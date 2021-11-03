from django.urls import path
from . import views


urlpatterns = [
    path('', views.TodoHomeView.as_view(), name='todo-home'),
]
