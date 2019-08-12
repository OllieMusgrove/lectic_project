from django.conf.urls import url 
from lectic import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^quiz_selection/$', views.quiz_selection, name='quiz_selection'),
    url(r'^add_quiz/$', views.add_quiz, name='add_quiz'),
    url(r'^(?P<quiz_name_slug>[\w\-]+)/add_question/$', views.add_question, name='add_question'),
    url(r'^(?P<quiz_name_slug>[\w\-]+)/game/(?P<question_number>[0-9]{1})/(?P<quiz_attempt_no>[0-9]{7})/$', views.game, name='game'),
    url(r'^(?P<quiz_name_slug>[\w\-]+)/leaderboard/$', views.leaderboard, name='leaderboard'), 
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
]
