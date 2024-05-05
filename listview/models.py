from django.db import models
from django.forms import ModelForm, Textarea
from storages.backends.s3boto3 import S3Boto3Storage

# Create your models here.

class Client(models.Model):
  STATUS = (
        ('Hold', 'Hold'),
        ('Progress', 'Progress'),
        ('Review', 'Review'),
        ('Approved', 'Approved')
    )
  id = models.AutoField(primary_key=True)
  certificate_name = models.CharField(max_length=250,null=True)
  title=models.CharField(max_length=100,null=True)
  certificate_type=models.CharField(max_length=250,null=True)
  name = models.CharField(max_length=150, null=True)
  company = models.CharField(max_length=250,null=True)
  phone = models.CharField(max_length=10, null=True) 
  date = models.DateField(auto_now_add=True)  
  task_status=models.CharField(max_length=10, null=True,default='Hold', choices= STATUS)
  description = models.TextField(blank=True, null=True)
  user_mail=models.EmailField(max_length=150,null=True)
  flookup_description=models.TextField(blank=True, null=True)
  upload= models.TextField(null=True,default='N')
  flookup_uploads=models.TextField(null=True,default='N')


  def __str__(self):
    return f'{ self.name }'

class Login_Details(models.Model):
  u_name = models.CharField(max_length=40)
  u_email = models.EmailField(max_length=40, primary_key=True)
  u_pass = models.CharField(max_length=40)
  u_access = models.CharField(max_length=40)

  def __str__(self):
    return f'{ self.u_name }'

class Base_Email(models.Model):
  b_name = models.CharField(max_length=40)
  b_email = models.EmailField(max_length=40)
  b_pass = models.CharField(max_length=40, null=True)

  def __str__(self):
    return f'{ self.b_name }'


class MediaStorage(S3Boto3Storage):
    location = 'Records'
    file_overwrite = True