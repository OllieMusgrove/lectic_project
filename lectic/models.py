from django.db import models
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
import uuid

import os

# Create your models here.

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
    # time = models.DecimalField(decimal_places = 3, max_digits = 5)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.question)
        super(Question, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'questions'

    def __str__(self):
        return self.question


class QuestionAttempt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question)
    attempt = models.CharField(max_length=100, unique=False)
    result = models.BooleanField()

    def save(self, *args, **kwargs):
        if self.question.answer == self.attempt:
            self.result = True
            print ('Correct Answer!')
        else:
            self.result = False
            print ('Wrong Answer!')
        super(QuestionAttempt, self).save(*args, **kwargs)

    def __str__(self):
        return self.id