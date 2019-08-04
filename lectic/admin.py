from django.contrib import admin
from lectic.models import Question
from lectic.models import Quiz
from lectic.models import QuestionAttempt
from lectic.models import QuizAttempt

class QuizAdmin(admin.ModelAdmin):
    list_display = ('name',)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer','quiz')

class QuestionAttemptAdmin(admin.ModelAdmin):    
    list_display = ('time_stamp', 'id', 'question','attempt','result','time','quiz_attempt')
    ordering = ('-time_stamp',)

class QuizAttemptAdmin(admin.ModelAdmin):    
    list_display = ('created_datetime', 'auto_id')
    ordering = ('-created_datetime',)

# Register your models here.
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionAttempt, QuestionAttemptAdmin)
admin.site.register(QuizAttempt, QuizAttemptAdmin)
