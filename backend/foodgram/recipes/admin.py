from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class RecipeAdmin(admin.ModelAdmin):
    list_filter = ('author', 'title', 'tag')


class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('name')


models = apps.get_app_config('recipes').get_models()
for model in models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
