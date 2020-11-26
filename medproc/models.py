from django.db import models

# Create your models here.


class Document(models.Model):
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Appointment(models.Model):
    date = models.CharField(max_length=20)
    symptom = models.CharField(max_length=100)
    diagnosis = models.CharField(max_length=100)


class Dates(models.Model):
    startdate = models.CharField(max_length=20)
    enddate = models.CharField(max_length=20)
