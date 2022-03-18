from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from django_countries import Countries
from .managers import CustomUserManager
from django.core.validators import RegexValidator

class MyUser(AbstractUser):
    username = None
    email = models.EmailField(("email address"), unique=True)
    confirmation_code = models.CharField(max_length=40)
    email_confirmed = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images', blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email




class Customer_Address(models.Model):

    class CountriesList(Countries):
        only = [
            'CA', 'US'
            ]

    customer = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    street = models.CharField(max_length=120, blank=False)
    city  = models.CharField(max_length=40, blank=False)
    postcode = models.CharField(max_length=7, blank=False)
    country = CountryField(blank=False, default='CA', countries = CountriesList)
    phone_number = models.CharField(blank=False, max_length=12, validators=[RegexValidator(r'^\d{1,10}$')])
