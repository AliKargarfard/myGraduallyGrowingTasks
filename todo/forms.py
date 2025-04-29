from django import forms
from .models import Task

# Reordering Form and View


class TaskUpdateForm(forms.ModelForm):
    task_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control rounded-4",
                "name": "task_name",
                "placeholder": "Task Name",
            }
        ),
        label="",
    )

    class Meta:
        model = Task
        fields = ("task_name",)
