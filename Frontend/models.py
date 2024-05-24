from django.db import models

# Create your models here.
class Registration(models.Model):
    username=models.CharField(max_length=50,null=True,blank=True)
    Email=models.EmailField(max_length=50,null=True,blank=True)
    Password=models.CharField(max_length=50,null=True,blank=True)