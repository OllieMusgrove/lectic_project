from django.contrib import admin
from lectic.models import Question
from lectic.models import Quiz


class QuizAdmin(admin.ModelAdmin):
    list_display = ('name',)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer','quiz')



# Register your models here.
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
