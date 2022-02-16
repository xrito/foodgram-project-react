import os
import uuid

from django.db import models
from django.conf import settings
from django.utils.html import format_html


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
    title = models.CharField(
        max_length=255,
        choices=DEFAULT_CHOICES,
        default='breakfast',
        blank=False
    )
    hexcolor = models.CharField(
        max_length=7,
        default='#49B64E',
        verbose_name='Цвет тега',
        help_text=(u'HEX color, as #RRGGBB')
    )
    slug = models.SlugField(
        max_length=255,
        default='',
        # editable=False,
        unique=True,
        db_index=True,
        verbose_name='URL'
    )

    def colored_title(self):
        return format_html(
            '<span style="color: #{};">{}</span>',
            self.hexcolor,
        )

    def __str__(self):
        return self.title


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


class Recipe(models.Model):
    """Recipe object"""
    title = models.CharField(
        max_length=255,
        verbose_name='Название рецепта')
    tag = models.ManyToManyField(
        Tag,
        blank=False,
        related_name='recipes',
        verbose_name='Теги'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        blank=True,
        # null=True,
        through='IngredientToRecipe',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингридиенты'
    )
    time_minutes = models.IntegerField(
        verbose_name='Время приготовления',
        help_text='минут'
    )
    text = models.TextField(verbose_name='Описание')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публицации'
    )
    image = models.ImageField(
        'Фото',
        upload_to=recipe_image_file_path,
        blank=True,
        null=True,
        help_text='Загрузите фото'
    )
    
    def get_ingredients(self):
        return ", ".join([p.name for p in self.ingredients.all()])
    
    class Meta:
        models.UniqueConstraint(
            fields=['title', 'author'], name='unique_review')
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ('pub_date',)

    def __str__(self):
        return '{}, {}'.format(self.title, self.author)


class IngredientToRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        null=True,
        on_delete=models.SET_NULL
    )
    recipe = models.ForeignKey(
        Recipe,
        null=True,
        on_delete=models.SET_NULL
    )
    quantity = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Количество'
    )
    
    def __str__(self):
        return '{}'.format(self.recipe)    