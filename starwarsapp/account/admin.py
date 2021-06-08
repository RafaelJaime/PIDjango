from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, UserCalification
# Register your models here.


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        *BaseUserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            # group heading of your choice; set to None for a blank space instead of a header
            'Specialities: ',
            {
                'fields': (
                    'is_newsPaperman',
                    'favorite_films',
                    'favorite_characters'
                ),
            },
        ),
    )
    search_fields = ['username', 'first_name', 'last_name']
    list_display = ('id', 'username', 'first_name', 'last_name', 'is_newsPaperman', 'is_superuser')
    list_filter = ['is_superuser', 'is_newsPaperman', 'is_active']
admin.site.register(User, UserAdmin)
admin.site.register(UserCalification)