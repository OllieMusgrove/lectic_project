from django.contrib import admin
from lectic.models import Question
from lectic.models import Quiz, Module
from lectic.models import QuestionAttempt
from lectic.models import QuizAttempt
from lectic.models import UserProfile

class QuizAdmin(admin.ModelAdmin):
    list_display = ('name','level','module')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer','quiz')

class QuestionAttemptAdmin(admin.ModelAdmin):    
    list_display = ('time_stamp', 'question','attempt','result','time','quiz_attempt','performance')
    ordering = ('-time_stamp',)

class QuizAttemptAdmin(admin.ModelAdmin):    
    list_display = ('user','quiz','created_datetime', 'auto_id', 'performance','accumulated_score', 'qes_possible','qes_complete','finished','all_correct','merit','distinction')
    ordering = ('-created_datetime',)

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name',)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'matric_number', 'coins', 'is_lecturer')

# Register your models here.
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionAttempt, QuestionAttemptAdmin)
admin.site.register(QuizAttempt, QuizAttemptAdmin)
admin.site.register(UserProfile)
admin.site.register(Module,ModuleAdmin)
