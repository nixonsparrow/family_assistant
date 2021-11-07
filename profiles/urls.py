from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProfileView.as_view(), name='profile'),
    path('edit/', views.ProfileUpdateView.as_view(), name='edit-profile'),
]
