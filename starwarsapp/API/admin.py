from django.contrib import admin
from .models import Article, Event, Post, Answer, Product, Film, FilmCommentary, Character, CharacterCommentary, Ranking, Onboarding

# Register your models here.

# Tabbar
# Pantalla1
# class ArticleAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'author', 'event')
#     search_fields = ['title', 'author']
#     list_filter = ['author']
# admin.site.register(Article, ArticleAdmin)
# class EventAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'telephone', 'email', 'startDate')
#     search_fields = ['title', 'description']
# admin.site.register(Event, EventAdmin)

# Pantalla2
admin.site.register(Post)
admin.site.register(Answer)

# Pantalla3
admin.site.register(Product)

# Pantalla4


# Ranking
admin.site.register(Ranking)

# Peliculas
admin.site.register(Film)
admin.site.register(FilmCommentary)

# Personajes
admin.site.register(Character)
admin.site.register(CharacterCommentary)

# General
# Onboarding
admin.site.register(Onboarding)