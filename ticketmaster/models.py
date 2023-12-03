from django.db import models


# Create your models here.


class Ticket(models.Model):
    # class that describes ticket objects user can purchase
    Name = models.CharField(max_length=150)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)


class Person(models.Model):
    # class that person object
    userName = models.CharField(max_length=50)
    passWord = models.CharField(max_length=50)
    eventCart = models.DecimalField(max_digits=9, decimal_places=2)
