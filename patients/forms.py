from django import forms

from patients.models import Question


class QuestionForm(forms.ModelForm):
    class Meta :
        model = Question 
        fields = ['question_text']
        