"""family_assistant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from todo.views import Homepage
from profiles.views import RegisterView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo.urls')),
    path('', Homepage.as_view(), name='homepage'),

    path('profile/', include('profiles.urls')),

    # authentication paths
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html', extra_context={'extra_title': 'Log In'}), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='auth/logout.html', extra_context={'extra_title': 'Logout'}), name='logout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='profiles/password_reset.html'),
         name='password_reset'),
    path('password-reset-done',
         auth_views.PasswordResetDoneView.as_view(template_name='profiles/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='profiles/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetView.as_view(template_name='profiles/password_reset_complete.html'),
         name='password_reset_complete'),
]
