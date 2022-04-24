import math
from turtle import update
from django.db import models

class Report(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='uploads/products/')
    remarks = models.TextField()
    created = models.DateTimeField(auto_now_add=True)   
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)