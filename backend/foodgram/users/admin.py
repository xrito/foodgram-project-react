from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class UserAdmin(admin.ModelAdmin):
    list_filter = ('username', 'email', 'first_name', 'second_name',)
    list_display = ('username', 'email', 'first_name', 'second_name',)
    search_fields = ('first_name', 'second_name')


admin.site.register(User, UserAdmin)
