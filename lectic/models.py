from django.db import models
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
import datetime
import uuid

from django.contrib.auth.models import User

import os

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    is_lecturer = models.BooleanField(default='False')
    matric_number = models.CharField(max_length=8, unique=False)

    def save(self, *args, **kwargs):
        if (self.matric_number == "LECTURER"):
            self.is_lecturer = True
        else:
            self.is_lecturer = False
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

class Quiz(models.Model):
    name = models.CharField(max_length=100, unique=False)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Quiz, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'quizzes'

    def __str__(self):
        return self.name


class Question(models.Model):
    question = models.CharField(max_length=1000, unique=False)
    answer = models.CharField(max_length=100)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.question)
        super(Question, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'questions'

    def __str__(self):
        return self.question


class QuizAttempt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auto_id = models.IntegerField(default=3000000)
    created_datetime = models.DateTimeField(default=datetime.datetime.now)
    performance = models.DecimalField(decimal_places = 3, max_digits = 10, default=0.000, editable=True)
    accumulated_score = models.IntegerField(default=0)
    qes_possible = models.IntegerField(default=0)
    qes_complete = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)
    all_correct = models.BooleanField(default=False, editable=True)
    merit = models.BooleanField(default=False, editable=True)
    distinction = models.BooleanField(default=False, editable=True)
    user = models.ForeignKey(User)
    quiz = models.ForeignKey(Quiz)

    def save(self, *args, **kwargs):
        if self.qes_possible == self.qes_complete and self.qes_possible != 0:
            self.finished = True
            if self.accumulated_score == self.qes_possible:
                self.all_correct = True
                if self.performance <= self.qes_possible*10:
                    self.merit = True
                    if self.performance <= self.qes_possible*5:
                        self.distinction = True
                    else:
                        self.distinction = False
                else:
                    self.merit = False
            else:
                self.all_correct = False
        else:
            self.finished = False
        super(QuizAttempt, self).save(*args, **kwargs)

    def __int__(self):
        return self.auto_id


class QuestionAttempt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time_stamp = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question)
    attempt = models.CharField(max_length=100, unique=False)
    time = models.DecimalField(decimal_places = 3, max_digits = 6, default=0.000)
    result = models.BooleanField()
    quiz_attempt = models.ForeignKey(QuizAttempt)
    performance = models.DecimalField(decimal_places = 3, max_digits = 10, default=0.000)

    def save(self, *args, **kwargs):
        if self.question.answer == self.attempt:
            self.result = True
            self.performance = self.time
            print ('Correct Answer!')
        else:
            self.result = False
            self.performance = self.time + 10
            # self.performance = self.time
            print ('Wrong Answer!')
        super(QuestionAttempt, self).save(*args, **kwargs)

    def __str__(self):
        return self.id


class Module(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Module, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'modules'

    def __str__(self):
        return self.name