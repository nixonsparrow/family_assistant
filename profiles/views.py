from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm

    def get_context_data(self, **kwargs):
        return {
            'extra_title': 'Register User',
            'form': self.get_form()
        }

    def get_success_url(self):
        return reverse_lazy('homepage')


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'profiles/profile.html'

    def get_context_data(self, **kwargs):
        return {
            'extra_title': 'Profile',
        }

    def get_object(self, **kwargs):
        return get_object_or_404(User, username=self.request.user.username)

    def test_func(self):
        if self.request.user == self.get_object():
            return True
        return False


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'profiles/edit_profile.html'
    form_class = UserUpdateForm

    def get_context_data(self, **kwargs):
        return {
            'extra_title': 'Edit Profile',
            'form': self.get_form()
        }

    def get_object(self, **kwargs):
        return get_object_or_404(User, username=self.request.user.username)

    def test_func(self):
        if self.request.user == self.get_object():
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('profile')
