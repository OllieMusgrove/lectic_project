from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from datetime import datetime
from lectic.models import Question, Quiz, QuestionAttempt, QuizAttempt, UserProfile, User, Module
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

def about(request):
    return render(request, 'lectic/about.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def quiz_selection(request):
    try:
        quiz_list = Quiz.objects.all().order_by('level')
    except Quiz.DoesNotExist:
        quiz_list = None
    
    try:
        module_list = Module.objects.all()
    except Module.DoesNotExist:
        module_list = None
    
    # try:
    #     module_available = Module.objects.all()
    #     quiz_available = Quiz.objects.filter(module=module_available)
    #     # distinct_quiz_mod = [quiz_available.filter(module=item['module']) for item in quiz_available.values('module').distinct]
    #     # module_available = Module.objects.filter(name_in=quiz_available)
    #     # item_list = [all_qz_attempts.filter(user=item['user']).last() for item in UserProfile.objects.filter(is_lecturer=False).values('user').distinct()]
    #     print (module_available)
    #     print (quiz_available)
    #     # print (distinct_quiz_mod)

    except Quiz.DoesNotExist:
        module_list = None

    user_profile = UserProfile.objects.get(user=request.user)
    coins = user_profile.coins
    unlocked = int (coins/10)+1

    context_dict = {'unlocked': unlocked,'coins': coins,'modules': module_list, 'quizzes': quiz_list}
    return render(request, 'lectic/quiz_selection.html', context_dict)

@login_required
def game(request, quiz_name_slug, question_number, quiz_attempt_no):
    
    quiz_attempt_int = int (quiz_attempt_no)

    quiz_attempt = QuizAttempt()
    if quiz_attempt_int == 0000000:
        quiz_attempt = QuizAttempt()
        quiz_attempt.user = request.user
        quiz_attempt.quiz = Quiz.objects.get(slug=quiz_name_slug)
        try:
            next_quizattempt = QuizAttempt.objects.latest('created_datetime')
            quiz_attempt.auto_id = next_quizattempt.auto_id + 1
            quiz_attempt_int = quiz_attempt.auto_id
            quiz_attempt.save()
        except QuizAttempt.DoesNotExist:
            quiz_attempt.auto_id = 1000000
            quiz_attempt_int = quiz_attempt.auto_id
            quiz_attempt.save()
    else:
        quiz_attempt = QuizAttempt.objects.get(auto_id=quiz_attempt_int)
        quiz_attempt_int = quiz_attempt.auto_id
        # user_profile = UserProfile.objects.get(user=request.user)
        # user_profile.coins = user_profile.coins + quiz_attempt.coins
        # user_profile.save()
        # print ("coins added")
        # print (user_profile.coins)
    
    if quiz_attempt_int == 0000000:
        quiz_attempt_no = "0000000"
    else:
        quiz_attempt_no = str (quiz_attempt_int)
    
    quest_num = int (question_number)
    display_num = quest_num + 1

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
        print("attempt =" + attempt)
        print("elapsed time = " + elapsed_time)
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

    try:
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.coins = user_profile.coins + quiz_attempt.coins
        user_profile.save()
        print ("coins added")
        print (user_profile.coins)

    except:
        print ("no user found")


    qn_plus = quest_num #may need exception handling...
    progress = int ((qn_plus/question_list.count())*100)

    context_dict = {'q_num_display': display_num, 'progress': progress, 'questions': question_list, 'question_select': question_select,'question_number': quest_num, 'quiz_attempt' : quiz_attempt, 'init_quiz' : quiz_attempt_no}
    return render(request, 'lectic/game.html', context_dict)

@login_required
def add_quiz(request):
    
    try:
        quiz_list = Quiz.objects.all().order_by('level')
    except Quiz.DoesNotExist:
        quiz_list = None
    
    try:
        module_list = Module.objects.all()
    except Quiz.DoesNotExist:
        module = None

    form = QuizForm()
    if request.method == 'POST':
        form = QuizForm(request.POST)

        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.save()
            # return add_quiz(request) <- makes recursion error       
        else:
            print(form.errors)    
    
    context_dict = {'modules':module_list,'quizzes': quiz_list, 'form': form}    
    return render(request, 'lectic/add_quiz.html', context_dict)

@login_required
def add_question(request, quiz_name_slug):
    try:
        quiz_select = Quiz.objects.get(slug=quiz_name_slug)
        questions = Question.objects.filter(quiz=quiz_select)
    except Quiz.DoesNotExist:
        quiz_select = None
        questions = None

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

    context_dict = {'questions': questions, 'quiz': quiz_select, 'form': form}    
    return render(request, 'lectic/add_question.html', context_dict)

@login_required
def leaderboard(request, quiz_name_slug):
    try:
        quiz_select = Quiz.objects.get(slug=quiz_name_slug)
    except Quiz.DoesNotExist:
        quiz_select = None

    try:
        all_qz_attempts = QuizAttempt.objects.exclude(finished=False).filter(quiz=quiz_select)
        print (all_qz_attempts.count())
        if (all_qz_attempts.count() != 0):
            all_qz_attempts = QuizAttempt.objects.exclude(finished=False).filter(quiz=quiz_select).order_by('-performance')
            uu1 = UserProfile.objects.filter(is_lecturer=False).values('user').distinct()
            item_list = [all_qz_attempts.filter(user=item['user']).last() for item in UserProfile.objects.filter(is_lecturer=False).values('user').distinct()]
            ordered_il = sorted(item_list, key=lambda x: x.performance, reverse=False)
            print(all_qz_attempts)
            print(uu1)
            print(item_list)
            print(ordered_il)
        else:
            ordered_il = None
    except QuizAttempt.DoesNotExist:
        ordered_il = None

    context_dict = {'quiz_attempts' : ordered_il}    
    return render(request, 'lectic/leaderboard.html', context_dict)

@login_required
def quiz_end(request, quiz_name_slug, quiz_attempt_no):
    
    quiz_select = Quiz.objects.get(slug=quiz_name_slug)
    quiz_attempt = QuizAttempt.objects.get(auto_id=quiz_attempt_no)

    all_qz_attempts = QuizAttempt.objects.exclude(finished=False).filter(quiz=quiz_select).order_by('-performance')
    best_user_performances = [all_qz_attempts.filter(user=item['user']).last() for item in UserProfile.objects.filter(is_lecturer=False).values('user').distinct()]
    print (best_user_performances)
    best_user_performances = filter(None,best_user_performances)
    print (best_user_performances)
    ranked_by_user = sorted(best_user_performances, key=lambda x: x.performance, reverse=False)
    print (ranked_by_user)
    total_quiz_user_attempts = len(ranked_by_user)
    print (total_quiz_user_attempts)

    outOf = all_qz_attempts.count()
    attempt = QuizAttempt.objects.exclude(finished=False).filter(user=request.user).filter(quiz=quiz_select).count()

#calculates quiz attempt performace relative to all completed quizzes
    i = 0
    for item in QuizAttempt.objects.exclude(finished=False).filter(quiz=quiz_select).order_by('performance'):
        i += 1
        if item.auto_id == int (quiz_attempt_no):
            break

    # pb = quiz_attempt
#calculates user performace for quiz-select
    for performance in best_user_performances:
        if performance.user == request.user:
            pb = performance
            print ("pb found")
            break

    j = 0
    for qa in ranked_by_user:
        j += 1
        if qa.auto_id == pb.auto_id:
            print ("match found")
            print (j)
            break


    context_dict = {'tot_class':total_quiz_user_attempts,'pos_inclass': j,'pb':pb,'attempt':attempt,'quiz_attempt' : quiz_attempt, 'quiz_slug' : quiz_name_slug, 'pos' : i, 'tot' : outOf}    
    return render(request, 'lectic/quiz_end.html', context_dict)

@login_required
def delete(request, quiz_name_slug, question_name_slug):
    quiz_select = Quiz.objects.get(slug=quiz_name_slug)
    object = Question.objects.get(slug=question_name_slug, quiz=quiz_select)
    # except Question.DoesNotExist: <- add exception handling
    # except Question.MultipleObjectsReturned:
    object.delete()
    return add_question(request,quiz_name_slug)