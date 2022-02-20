import os
import uuid

from django.db import models
from django.conf import settings
from django.utils.html import format_html
from users.models import User
from django.db.models import UniqueConstraint

def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/recipe/', filename)


class Tag(models.Model):
    """Tag to be used for a recipe"""
    DEFAULT_CHOICES = (
        ('breakfast', 'Завтрак'),
        ('dinner', 'Обед'),
        ('supper', 'Ужин'),
    )
    name = models.CharField(
        max_length=255,
        choices=DEFAULT_CHOICES,
        default='breakfast',
        blank=False
    )
    color = models.CharField(
        max_length=7,
        default='#49B64E',
        verbose_name='Цвет тега',
        help_text=(u'HEX color, as #RRGGBB')
    )
    slug = models.SlugField(
        max_length=255,
        default='',
        unique=True,
        db_index=True,
        verbose_name='URL'
    )

    def colored_title(self):
        return format_html(
            '<span style="color: #{};">{}</span>',
            self.color,
        )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe object"""
    tags = models.ManyToManyField(
        Tag,
        blank=False,
        related_name='recipes',
        verbose_name='Теги'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    ingredient = models.ManyToManyField(
        'Ingredient',
        # blank=False,
        through='IngredientinRecipe',
        # through_fields=('recipe', 'ingredient'),
        related_name='recipes',
        verbose_name='Ингридиенты'
    )
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публицации'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Название рецепта')
    image = models.ImageField(
        'Фото',
        upload_to=recipe_image_file_path,
        blank=True,
        null=True,
        help_text='Загрузите фото'
    )
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        help_text='минут'
    )
    users = models.ManyToManyField(
        User,
        related_name='favorite_recipe'
    )

    def get_ingredient(self):
        return ", ".join([p.name for p in self.ingredient.all()])

    class Meta:
        models.UniqueConstraint(
            fields=['name', 'author'], name='unique_review')
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ('-pub_date',)

    def __str__(self):
        return '{}, {}'.format(self.name, self.author)


class Ingredient(models.Model):
    """Ingredient to be used in a recipe"""
    name = models.CharField(
        max_length=255,
        db_index=True,
        blank=False,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=255,
        blank=False,
        verbose_name='Единицы измерения'
    )

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return '{}, {}'.format(self.name, self.measurement_unit)


class IngredientinRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        null=True,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        null=True,
        on_delete=models.SET_NULL,
        related_name='ingredient_recipes'
    )
    amount = models.IntegerField(
        blank=False,
        null=False,
        verbose_name='Количество'
    )

    def __str__(self):
        return '{}'.format(self.recipe)


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             )
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE
                               )
    class Meta:
        unique_together = ('user', 'recipe')
        UniqueConstraint(
            fields=['user', 'recipe'], name='unique_favorite')