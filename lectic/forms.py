from django import forms
from lectic.models import Question
from lectic.models import Quiz

class QuestionForm(forms.ModelForm):
    question = forms.CharField(max_length=1000, help_text="Please enter a question")
    answer = forms.CharField(max_length=100, help_text="Please enter the answer")

    class Meta:
        model = Question
        fields = ('question','answer')


class QuizForm(forms.ModelForm):
    name = forms.CharField(max_length=100, help_text="Please enter a quiz name")

    class Meta:
        model = Quiz
        fields = ('name',)

