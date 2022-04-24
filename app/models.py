# models.py
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models


class Patient(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    city = models.CharField(max_length=255)
    appointment_date = models.DateTimeField()
    appointment_details = models.TextField()

    def __str__(self):
        return self.name
