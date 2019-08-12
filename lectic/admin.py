from django.contrib import admin
from lectic.models import Question
from lectic.models import Quiz
from lectic.models import QuestionAttempt
from lectic.models import QuizAttempt
from lectic.models import UserProfile

class QuizAdmin(admin.ModelAdmin):
    list_display = ('name',)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer','quiz')

class QuestionAttemptAdmin(admin.ModelAdmin):    
    list_display = ('time_stamp', 'question','attempt','result','time','quiz_attempt','performance')
    ordering = ('-time_stamp',)

class QuizAttemptAdmin(admin.ModelAdmin):    
    list_display = ('user','quiz','created_datetime', 'auto_id', 'performance','accumulated_score', 'qes_possible','qes_complete','finished','all_correct','merit','distinction')
    ordering = ('-created_datetime',)

# Register your models here.
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionAttempt, QuestionAttemptAdmin)
admin.site.register(QuizAttempt, QuizAttemptAdmin)
admin.site.register(UserProfile)
