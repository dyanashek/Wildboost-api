from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    expire_date = models.DateField(
        blank=True,
        null=True,
        default=None
    )
    subscribe_plan = models.IntegerField(
        blank=True,
        null=True,
        default=None
    )
    verified = models.BooleanField(
        default=False
    )

class Payment(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        related_name='payments',
        blank=True, 
        null=True
    )
    payment_id = models.CharField(max_length=200, unique=True)
    payment_status = models.BooleanField(
        blank=True,
        null=True,
        default=None
    )
    payment_amount = models.IntegerField()
    expire_date = models.DateField(
        blank=True,
        null=True,
        default=None
    )
    subscribe_plan = models.IntegerField(
        blank=True,
        null=True,
        default=None
    )
    payment_time = models.DateTimeField(auto_now_add=True)

class Update(models.Model):
    version = models.CharField(max_length=10)
    url = models.URLField()
    description = models.CharField(max_length=2000)
    important = models.BooleanField(default=False)
    creation_date = models.DateField(auto_now_add=True)

class Subscription(models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    adverts = models.IntegerField()
    products = models.IntegerField()
    renew = models.IntegerField()





#python3 manage.py migrate --run-syncdb
    


