from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from lectic.models import Question, Quiz, QuestionAttempt
from lectic.forms import QuestionForm, QuizForm, QuestionAttemptForm

def index(request):
    return render(request, 'lectic/index.html', {})

def quiz_selection(request):
    quiz_list = Quiz.objects.all
    context_dict = {'quizzes': quiz_list}
    return render(request, 'lectic/quiz_selection.html', context_dict)


def game(request, quiz_name_slug):
    
    question_list = None
    try:
        quiz = Quiz.objects.get(slug=quiz_name_slug)
        question_list = Question.objects.filter(quiz=quiz)
        question_select = Question.objects.filter(quiz=quiz).order_by('question')[0]
        print(question_list)
        print(question_select)
        
    except Quiz.DoesNotExist:
        question_list = None

    form = QuestionAttemptForm()
    if request.method == 'POST':
        form = QuestionAttemptForm(request.POST)

        if form.is_valid():
            question_attempt = form.save(commit=False)
            question_attempt.question = question_select
            question_attempt.save()     
        else:
            print(form.errors) 

    context_dict = {'questions': question_list, 'question_select': question_select, 'form': form}  
    return render(request, 'lectic/game.html', context_dict)


def add_quiz(request):
    
    try:
        quiz_list = Quiz.objects.all
    except Quiz.DoesNotExist:
        quiz_list = None
    
    form = QuizForm()
    if request.method == 'POST':
        form = QuizForm(request.POST)

        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.save()
            # return add_quiz(request) <- makes recursion error       
        else:
            print(form.errors)    
    
    context_dict = {'quizzes': quiz_list, 'form': form}    
    return render(request, 'lectic/add_quiz.html', context_dict)


def add_question(request, quiz_name_slug):
    try:
        quiz_select = Quiz.objects.get(slug=quiz_name_slug)
    except Quiz.DoesNotExist:
        quiz_select = None

    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz_select
            question.save()
            # url = "lectic/" + quiz_name_slug + "/add_question"
            # HttpResponseRedirect(url)    
        else:
            print(form.errors)      

    context_dict = {'quiz': quiz_select, 'form': form}    
    return render(request, 'lectic/add_question.html', context_dict)