from django import forms
from lectic.models import Question
from lectic.models import Quiz
from lectic.models import QuestionAttempt

from django.contrib.auth.models import User
from lectic.models import UserProfile

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


class QuestionAttemptForm(forms.ModelForm):
    attempt = forms.CharField(max_length=100, help_text="Please enter the answer")

    class Meta:
        model = QuestionAttempt
        fields = ('attempt',)