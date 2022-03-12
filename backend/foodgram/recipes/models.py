from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint


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
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            UniqueConstraint(fields=['name', 'measurement_unit'],
                             name='unique ingredient')
        ]

    def __str__(self):
        return '{}, {}'.format(self.name, self.measurement_unit)


class Tag(models.Model):
    """Tag to be used for a recipe"""
    PINK = '#FF80ED'
    ORANGE = '#FFA500'
    BLUE = '#000080'

    DEFAULT_CHOICES = [
        (PINK, 'Синий'),
        (ORANGE, 'Оранжевый'),
        (BLUE, 'Зеленый'),
    ]
    name = models.CharField(
        max_length=255,
        unique=True,
        default='breakfast',
        blank=False
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        choices=DEFAULT_CHOICES,
        default='#49B64E',
        verbose_name='Цвет тега',
        help_text=(u'HEX color, as #RRGGBB')
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name='URL'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

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
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientinRecipe',
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
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
        upload_to='recipes/',
        help_text='Фото рецепта'
    )
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), ],
        verbose_name='Время приготовления',
        help_text='минут'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)
        constraints = [
            UniqueConstraint(
                fields=['name', 'author'], name='unique_review')
        ]

    def get_ingredients(self):
        return ", ".join([p.name for p in self.ingredients.all()])

    def __str__(self):
        return '{}, {}'.format(self.name, self.author)


class IngredientinRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        null=True,
        on_delete=models.CASCADE,
        related_name='ingredient_recipes'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        null=True,
        on_delete=models.SET_NULL,
        related_name='ingredient_recipes'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), ],
        blank=False,
        null=False,
        verbose_name='Количество'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            UniqueConstraint(fields=['ingredient', 'recipe'],
                             name='unique ingredient in recipe')
        ]

    def __str__(self):
        return '{}'.format(self.recipe)


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorit',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт в избранном'
        verbose_name_plural = 'Рецепты в избранном'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favorite')
        ]


class CartRecipe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart'
    )

    class Meta:
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'Рецепты в корзине'
