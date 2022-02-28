from django.contrib import admin
from .models import User, Subscription
from django.contrib.auth.admin import UserAdmin


class UserAdmin(admin.ModelAdmin):
    list_filter = ('username', 'email', 'first_name', 'last_name',)
    list_display = ('username', 'email', 'first_name', 'last_name',)
    search_fields = ('first_name', 'last_name')


class SubscriptionAdmin(admin.ModelAdmin):
    model = Subscription


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(User, UserAdmin)
