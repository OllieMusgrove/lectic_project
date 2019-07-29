from django.conf.urls import url 
from lectic import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^quiz_selection/$', views.quiz_selection, name='quiz_selection'),
    url(r'^add_quiz/$', views.add_quiz, name='add_quiz'),
    url(r'^(?P<quiz_name_slug>[\w\-]+)/add_question/$', views.add_question, name='add_question'),
    url(r'^(?P<quiz_name_slug>[\w\-]+)/game/$', views.game, name='game'),
]
