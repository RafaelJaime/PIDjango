from django.contrib import admin
from .models import Article, Event, Product

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'event')
    search_fields = ['title', 'author']
    list_filter = ['author']
admin.site.register(Article, ArticleAdmin)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'telephone', 'email', 'startDate')
    search_fields = ['title', 'description']
admin.site.register(Event, EventAdmin)
admin.site.register(Product)