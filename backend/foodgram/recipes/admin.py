from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from .models import Recipe, Tag, Ingredient, IngredientToRecipe


class TagAdmin(admin.ModelAdmin):
    list_filter = ('recipes',)
    prepopulated_fields = {'slug': ('title',)}
class IngredientToRecipeInline(admin.TabularInline):
    model = IngredientToRecipe

class RecipeAdmin(admin.ModelAdmin):
    list_filter = ('author', 'title', 'tag')
    list_display = ('title', 'get_ingredients', 'author', 'pub_date')
    filter_horizontal = ('tag', 'ingredients')
    raw_id_fields = ('author',)
    date_hierarchy = 'pub_date'
    ordering = ('-pub_date',)
    inlines = [IngredientToRecipeInline]
    
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('measurement_unit',)


class IngredientToRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'quantity')
    list_filter = ('recipe',)
    raw_id_fields = ('recipe',)


admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientToRecipe, IngredientToRecipeAdmin)

# models = apps.get_app_config('recipes').get_models()
# for model in models:
#     try:
#         admin.site.register(model)
#     except AlreadyRegistered:
#         pass
