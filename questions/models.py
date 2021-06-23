from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length = 200)

    def __str__(self):
        return self.question_text

class Choices(models.Model):
    question = models.ManyToManyField(Question)
    choice_text = models.CharField(max_length = 200)
    #votes = models.ManyToManyField(User, blank = True, default=None)

    def __str__(self):
        return self.choice_text

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, default = 1)
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice = models.ForeignKey(Choices, on_delete = models.CASCADE)

    