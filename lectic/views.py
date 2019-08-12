from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from datetime import datetime
from lectic.models import Question, Quiz, QuestionAttempt, QuizAttempt, UserProfile
from lectic.forms import QuestionForm, QuizForm, QuestionAttemptForm, UserForm, UserProfileForm
from decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
    return render(request, 'lectic/register.html', context_dict)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("You do not have an active Lectic account")
        else:
            print("Invalid login details: {0}, {1}".format(username, password)) 
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'lectic/login.html', {})


def index(request):
    if request.user.is_authenticated:
        print(request.user)
        this_user = request.user
        userprofile = UserProfile.objects.get(user=this_user)
        print(userprofile)
        print(userprofile.is_lecturer)
        if userprofile.is_lecturer:
            perm = True
        else:
            perm = False
    else:
        perm = False
        print("No user logged in")
    context_dict = {'perm': perm}
    return render(request, 'lectic/index.html', context_dict)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def quiz_selection(request):
    quiz_list = Quiz.objects.all
    context_dict = {'quizzes': quiz_list}
    return render(request, 'lectic/quiz_selection.html', context_dict)

@login_required
def game(request, quiz_name_slug, question_number, quiz_attempt_no):
    
    quiz_attempt_int = int (quiz_attempt_no)

    quiz_attempt = QuizAttempt()
    if quiz_attempt_int == 0000000:
        quiz_attempt = QuizAttempt()
        try:
            next_quizattempt = QuizAttempt.objects.latest('created_datetime')
            quiz_attempt.auto_id = next_quizattempt.auto_id + 1
            quiz_attempt_int = quiz_attempt.auto_id
            quiz_attempt.save()
        except QuizAttempt.DoesNotExist:
            quiz_attempt.auto_id = 1000000
            quiz_attempt.save()
    else:
        quiz_attempt = QuizAttempt.objects.get(auto_id=quiz_attempt_int)
        quiz_attempt_int = quiz_attempt.auto_id
    
    if quiz_attempt_int == 0000000:
        quiz_attempt_no = "0000000"
    else:
        quiz_attempt_no = str (quiz_attempt_int)
    
    quest_num = int (question_number)

    question_list = None
    try:
        quiz = Quiz.objects.get(slug=quiz_name_slug)
        question_list = Question.objects.filter(quiz=quiz)
        question_select = Question.objects.filter(quiz=quiz).order_by('question')[quest_num]
        print(question_list)
        print(question_select)
        quiz_attempt.qes_possible = len(question_list)
        print(quiz_attempt.qes_possible)
        quiz_attempt.save()
    except Quiz.DoesNotExist:
        question_list = None
        quiz_attempt.qes_possible = 0

    if request.method == 'POST':
        attempt = request.POST.get('attempt', '')
        elapsed_time = request.POST.get('time', '')
        question_attempt = QuestionAttempt()
        question_attempt.question = question_select
        question_attempt.attempt = attempt
        question_attempt.time = Decimal(elapsed_time)
        question_attempt.quiz_attempt = quiz_attempt
        question_attempt.save()
        print(question_attempt.performance)
        quiz_attempt.performance = quiz_attempt.performance + question_attempt.performance
        if question_attempt.result == True:
            quiz_attempt.accumulated_score = quiz_attempt.accumulated_score + 1
        else:
            quiz_attempt.accumulated_score = quiz_attempt.accumulated_score + 0
        quiz_attempt.qes_complete = quiz_attempt.qes_complete + 1
        quiz_attempt.save()
        print(quiz_attempt.performance)

    context_dict = {'questions': question_list, 'question_select': question_select,'question_number': quest_num, 'quiz_attempt' : quiz_attempt, 'init_quiz' : quiz_attempt_no}
    return render(request, 'lectic/game.html', context_dict)

@login_required
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

@login_required
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