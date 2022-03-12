from django.contrib import admin


from .models import (CartRecipe, FavoriteRecipe, Ingredient,
                     IngredientinRecipe, Recipe, Tag)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    list_filter = ('recipes',)
    prepopulated_fields = {'slug': ('name',)}


class IngredientinRecipeInline(admin.TabularInline):
    model = IngredientinRecipe


class RecipeAdmin(admin.ModelAdmin):
    list_filter = ('author', 'tags')
    list_display = ('name', 'author', 'is_favorited',
                    'get_ingredients',  'pub_date')
    search_fields = ('author', 'name', 'tags')
    filter_horizontal = ('tags', 'ingredients')
    raw_id_fields = ('author',)
    date_hierarchy = 'pub_date'
    ordering = ('-pub_date',)
    inlines = [IngredientinRecipeInline]

    def is_favorited(self, obj):
        return obj.favorite.count()


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('measurement_unit',)


class IngredientinRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
    list_filter = ('recipe',)
    raw_id_fields = ('recipe',)


class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class CartRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


admin.site.register(CartRecipe, CartRecipeAdmin)
admin.site.register(FavoriteRecipe, FavoriteRecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientinRecipe, IngredientinRecipeAdmin)
