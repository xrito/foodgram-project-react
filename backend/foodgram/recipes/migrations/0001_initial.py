# Generated by Django 2.2.16 on 2022-02-18 13:31

from django.db import migrations, models
import recipes.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='Название')),
                ('measurement_unit', models.CharField(max_length=255, verbose_name='Единицы измерения')),
            ],
            options={
                'verbose_name': 'Ingredient',
                'verbose_name_plural': 'Ingredients',
            },
        ),
        migrations.CreateModel(
            name='IngredientinRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='Количество')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_favorited', models.BooleanField(default=False)),
                ('is_in_shopping_cart', models.BooleanField(default=False)),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публицации')),
                ('name', models.CharField(max_length=255, verbose_name='Название рецепта')),
                ('image', models.ImageField(blank=True, help_text='Загрузите фото', null=True, upload_to=recipes.models.recipe_image_file_path, verbose_name='Фото')),
                ('text', models.TextField(verbose_name='Описание')),
                ('cooking_time', models.IntegerField(help_text='минут', verbose_name='Время приготовления')),
            ],
            options={
                'verbose_name': 'Recipe',
                'verbose_name_plural': 'Recipes',
                'ordering': ('pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('breakfast', 'Завтрак'), ('dinner', 'Обед'), ('supper', 'Ужин')], default='breakfast', max_length=255)),
                ('color', models.CharField(default='#49B64E', help_text='HEX color, as #RRGGBB', max_length=7, verbose_name='Цвет тега')),
                ('slug', models.SlugField(default='', max_length=255, unique=True, verbose_name='URL')),
            ],
        ),
    ]
