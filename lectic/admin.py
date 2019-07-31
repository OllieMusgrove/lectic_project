from django.contrib import admin
from lectic.models import Question
from lectic.models import Quiz
from lectic.models import QuestionAttempt

class QuizAdmin(admin.ModelAdmin):
    list_display = ('name',)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer','quiz')

class QuestionAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'question','attempt','result','time')

# Register your models here.
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionAttempt, QuestionAttemptAdmin)
