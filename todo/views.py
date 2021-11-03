from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, CreateView
from django.contrib import messages
from .models import Task
from .forms import NewTaskForm


class TasksListView(ListView):
    model = Task
    context_object_name = 'tasks'


class TaskCreateView(CreateView):
    model = Task
    form_class = NewTaskForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            messages.success(request, f'You have created a new task!')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('todo-all-tasks')
