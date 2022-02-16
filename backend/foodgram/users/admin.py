from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'username',)


admin.site.register(User, UserAdmin)
