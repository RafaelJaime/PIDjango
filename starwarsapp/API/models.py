from django.db import models
from django.conf import settings
from account.models import User

# 1h 2h en total
# TABBAR
# Primera pantalla (Noticias)
class Article(models.Model):
    title = models.CharField(max_length = 200)
    image = models.ImageField(upload_to = "Articles/", blank = True)
    subtitle = models.TextField(blank = True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    event = models.ForeignKey("API.Event", on_delete=models.CASCADE, blank = True, null = True)

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length = 200)
    image = models.ImageField(upload_to = "Events/", blank = True)
    latitude = models.DecimalField(max_digits = 30, decimal_places = 15, blank = True, null = True)
    longitude = models.DecimalField(max_digits = 30, decimal_places = 15, blank = True, null = True)
    telephone = models.DecimalField(max_digits = 15, decimal_places = 15, blank = True, null = True)
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
    answer = models.CharField(max_length = 200)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
        
# Tercera pantalla (Producto)
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
    is_selled = models.BooleanField(default = False)

# Cuarta pantalla (Chat)

# Ranking
class Ranking(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    film = models.ForeignKey("Film", on_delete = models.CASCADE)
    rank = models.IntegerField()
    class Meta:
        unique_together = (("film", "author"),)
        
# Peliculas
class Film(models.Model):
    title = models.CharField(max_length = 100)
    director = models.CharField(max_length = 100)
    producer = models.CharField(max_length = 100)
    sipnosis = models.TextField()
    image = models.ImageField(upload_to = "Films/", blank = True)
    release_date = models.DateField()
    characters = models.ManyToManyField("Character", related_name='characters', blank = True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True)
    # is_canon = models.BooleanField(default = True)
    
class FilmCommentary(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    film = models.ForeignKey("Film", on_delete = models.CASCADE)
    commentary = models.CharField(max_length = 200)
    class Meta:
        unique_together = (("author", "film"),)

# Personajes
class Character(models.Model):
    name = models.CharField(max_length = 100)
    actor = models.CharField(max_length = 100)
    biography = models.TextField()
    image = models.ImageField(upload_to = "Characters/", blank = True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True)

class CharacterCommentary(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    character = models.ForeignKey("Character", on_delete = models.CASCADE)
    commentary = models.CharField(max_length = 200)
    class Meta:
        unique_together = (("character", "author"),)

# General
# Onboarding
class Onboarding(models.Model):
    class OnboardingType(models.IntegerChoices):
        forRegisterUser = 1
        forNonRegisterUser = 2
        forNewsPaperMansUser = 3
        forAllUser = 4
    title = models.CharField(max_length = 100)
    image = models.ImageField(upload_to = "Onboarding/")
    forUsers = models.IntegerField(choices = OnboardingType.choices)
    showedTo = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True)