from django.db import models

# Create your models here.


class UserSignup(models.Model):
    username = models.CharField(max_length=20)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    password = models.TextField(max_length=10)
