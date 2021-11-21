from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    author = models.CharField(max_length=250, null=True)
    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=250)
    isbn = models.CharField(max_length=13)

    def __str__(self):
        return self.title

class Todo(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return self.title

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title