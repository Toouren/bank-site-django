from django.db import models
from django import forms


class Company(models.Model):
    company_id = models.IntegerField(primary_key=True)
    company_name = models.CharField(max_length=40)
    company_info = models.CharField(max_length=500)
    company_pic = models.ImageField(null=True)


class User(models.Model):
    login = models.CharField(max_length=15, primary_key=True)
    password = models.CharField(max_length=20)
    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)



# Create your models here.
