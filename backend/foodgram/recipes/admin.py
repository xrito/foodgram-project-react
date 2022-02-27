from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from .models import (CartRecipe, FavoriteRecipe, Ingredient,
                     IngredientinRecipe, Recipe, Tag, Subscribe)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    list_filter = ('recipes',)
    prepopulated_fields = {'slug': ('name',)}


class IngredientinRecipeInline(admin.TabularInline):
    model = IngredientinRecipe


class RecipeAdmin(admin.ModelAdmin):
    list_filter = ('author', 'name', 'tags')
    list_display = ('name', 'get_ingredient', 'author', 'pub_date')
    filter_horizontal = ('tags', 'ingredient')
    raw_id_fields = ('author',)
    date_hierarchy = 'pub_date'
    ordering = ('-pub_date',)
    inlines = [IngredientinRecipeInline]


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('measurement_unit',)


class IngredientinRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
    list_filter = ('recipe',)
    raw_id_fields = ('recipe',)


class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class CartRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
class SubscribeAdmin(admin.ModelAdmin):
    model =Subscribe

admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(CartRecipe, CartRecipeAdmin)
admin.site.register(FavoriteRecipe, FavoriteRecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientinRecipe, IngredientinRecipeAdmin)

# models = apps.get_app_config('recipes').get_models()
# for model in models:
#     try:
#         admin.site.register(model)
#     except AlreadyRegistered:
#         pass
