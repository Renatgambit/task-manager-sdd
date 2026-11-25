from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "status", "priority", "due_date"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Например, подготовить отчёт"}),
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "Подробности (необязательно)"}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }
