from django import forms
from lectic.models import Question
from lectic.models import Quiz
from lectic.models import QuestionAttempt, Module

from django.contrib.auth.models import User
from lectic.models import UserProfile

LEVELS_CHOICES = [tuple([x,x]) for x in range(1,10)]

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta: 
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm): 
    matric_number = forms.CharField(max_length=8, help_text="Please enter your matriculation number")

    class Meta:
        model = UserProfile
        fields = ('matric_number',)


class QuestionForm(forms.ModelForm):
    question = forms.CharField(max_length=1000, help_text="Please enter a question", label="Question: ")
    answer = forms.CharField(max_length=100, help_text="Please enter the answer", label="Answer: ")

    class Meta:
        model = Question
        fields = ('question','answer')


class QuizForm(forms.ModelForm):
    name = forms.CharField(max_length=100, help_text="Quiz Name: ")
    level = forms.IntegerField(widget=forms.Select(choices=LEVELS_CHOICES), help_text="Level: ")
    module = forms.ModelChoiceField(queryset=Module.objects.all(),
                                    to_field_name = 'name',
                                    empty_label="Select Module", help_text="Module: ")

    class Meta:
        model = Quiz
        fields = ('name','level','module')


class QuestionAttemptForm(forms.ModelForm):
    attempt = forms.CharField(max_length=100, help_text="Please enter the answer")

    class Meta:
        model = QuestionAttempt
        fields = ('attempt',)