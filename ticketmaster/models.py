from django.db import models


# Create your models here.


class Ticket(models.Model):
    # class that describes ticket objects user can purchase
    description = models.CharField(max_length=150)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
