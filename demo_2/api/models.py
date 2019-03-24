from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserInfo(AbstractUser):
    tel = models.CharField(max_length=32, null=True, blank=True)


class Book(models.Model):
    title = models.CharField(max_length=32)
    price = models.IntegerField()
    pub_date = models.DateField(null=True, blank=True)
    publish = models.ForeignKey("Publish", on_delete=models.CASCADE)
    authors = models.ManyToManyField("Author")

    def __str__(self):
        return self.title


class Publish(models.Model):
    name = models.CharField(max_length=32)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()

    def __str__(self):
        return self.name
