from django.db import models
from django.conf import settings
from account.models import User

# 1h 2h en total
# Create your models here.
# Primera pantalla (Noticias)
class Article(models.Model):
    title = models.CharField(max_length = 200)
    image = models.ImageField(upload_to = "Articles/", blank = True)
    subtitle = models.TextField(blank = True)
    content = models.TextField()
    event = models.ForeignKey("API.Event", on_delete=models.CASCADE, blank = True, null = True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length = 200)
    image = models.ImageField(upload_to = "Events/", blank = True)
    latitude = models.DecimalField(max_digits = 30, decimal_places = 15, blank = True, null = True)
    longitude = models.DecimalField(max_digits = 30, decimal_places = 15, blank = True, null = True)
    telephone = models.DecimalField(max_digits = 30, decimal_places = 15, blank = True, null = True)
    email = models.EmailField(max_length = 254, default = None)
    description = models.TextField(blank = True)
    startDate = models.DateField(auto_now = False, auto_now_add = False)
    endDate = models.DateField(auto_now = False, auto_now_add = False, blank = True, null = True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True)

# Segunda pantalla (Foro)
class Post(models.Model):
    title = models.CharField(max_length = 200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)

class Answer(models.Model):
    answer = title = models.CharField(max_length = 200)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
        
# Tercera pantalla
class Product(models.Model):
    name = models.CharField(max_length = 100)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    latitude = models.FloatField(blank = True, null = True)
    longitude = models.FloatField(blank = True, null = True)
    description = models.TextField()
    size = models.CharField(max_length = 50)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = "Products/")
    can_send = models.BooleanField(default = False)
    