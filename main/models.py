from django.db import models
from django.contrib.auth.models import User

class Info(models.Model):
    name = models.CharField(max_length=50, blank=False)
    ph = models.CharField(max_length=20, blank=False)
    message = models.TextField(blank=True)
    create_date = models.DateTimeField()
    agree = models.CharField(max_length=10, blank=False)

    def __str__(self):
        return self.name

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    info = models.ForeignKey(Info, on_delete=models.CASCADE)
    memo = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
