import email
from pyexpat import model
from statistics import mode
from turtle import title
from unicodedata import name
from venv import create
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Contact(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, null=True, blank= True)
    title = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length = 200)
    detail = models.TextField()
    is_active = models.BooleanField(default = True)

    def __str__(self):
        return self.title