from django.shortcuts import render, HttpResponseRedirect
from django.views.generic.edit import FormMixin
from django.views.generic import ListView
from .models import Task
from .forms import NewTaskForm


class TodoHomeView(ListView, FormMixin):
    model = Task
    template_name = 'todo/main.html'
    form_class = NewTaskForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if 'new_task' in form.data:
            Task.objects.create(title=form.data['new_task'])

        return HttpResponseRedirect('/todo/')
