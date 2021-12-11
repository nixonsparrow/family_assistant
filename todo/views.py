from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, CreateView, TemplateView, UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from .forms import NewTaskForm


class Homepage(TemplateView):
    template_name = 'homepage.html'
    extra_context = {'extra_title': 'Homepage'}


class TasksListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    extra_context = {'extra_title': 'Tasks'}


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = NewTaskForm
    extra_context = {'extra_title': 'New Task'}

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            messages.success(request, f'You have created a new task!')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('todo-all-tasks')


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = NewTaskForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['extra_title'] = self.object.title
        return context

    def get_success_url(self):
        return reverse_lazy('todo-all-tasks')

