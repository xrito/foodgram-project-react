# Generated by Django 2.2.16 on 2022-03-12 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartrecipe',
            options={'verbose_name': 'Рецепт в корзине', 'verbose_name_plural': 'Рецепты в корзине'},
        ),
        migrations.AlterModelOptions(
            name='favoriterecipe',
            options={'ordering': ['-id'], 'verbose_name': 'Рецепт в избранном', 'verbose_name_plural': 'Рецепты в избранном'},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'verbose_name': 'Ингредиент', 'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('-pub_date',), 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['-id'], 'verbose_name': 'Тег', 'verbose_name_plural': 'Теги'},
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='recipes.IngredientinRecipe', to='recipes.Ingredient', verbose_name='Ингредиенты'),
        ),
        migrations.AlterUniqueTogether(
            name='favoriterecipe',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='favoriterecipe',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_favorite'),
        ),
        migrations.AddConstraint(
            model_name='recipe',
            constraint=models.UniqueConstraint(fields=('name', 'author'), name='unique_review'),
        ),
    ]