from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    is_newsPaperman = models.BooleanField(default=False)
    favorite_films = models.ManyToManyField("API.Film", blank = True)
    favorite_characters = models.ManyToManyField("API.Character", blank = True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class UserCalification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'User')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='Author')
    calification = models.DecimalField(max_digits = 2, decimal_places = 0)
    
    class Meta:
        unique_together = (("user", "author"),)
