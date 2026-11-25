from django import forms

from .models import StudyCard


class StudyCardForm(forms.ModelForm):
    class Meta:
        model = StudyCard
        fields = ["subject", "topic", "question", "answer", "difficulty", "status", "next_review"]
        widgets = {
            "subject": forms.TextInput(attrs={"placeholder": "Например, История"}),
            "topic": forms.TextInput(attrs={"placeholder": "Например, Древняя Русь"}),
            "question": forms.TextInput(attrs={"placeholder": "Напишите вопрос для самопроверки"}),
            "answer": forms.Textarea(attrs={"rows": 5, "placeholder": "Запишите правильный ответ"}),
            "next_review": forms.DateInput(attrs={"type": "date"}),
        }
