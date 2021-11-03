from django import forms
from .models import Task


class NewTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Task Title'}),
        }
        fields = ['title']
