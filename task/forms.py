from task.models import Task
from django.db import models
from django.forms import ModelForm
from .models import Task


from django import forms


class TaskCreateForm(forms.Form):
    '''
    user create his task by using this form
    '''
    name = forms.CharField(widget=forms.Textarea,
                           label='Task name', max_length=300)
    done = forms.BooleanField(required=False, label='Completed')


class TaskUpdateForm(ModelForm):
    '''
    user edit his task by using this form
    '''
    class Meta:
        model = Task
        fields = ['name', 'done']
