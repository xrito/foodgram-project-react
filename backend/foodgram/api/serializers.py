from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (CartRecipe, FavoriteRecipe, Ingredient,
                            IngredientinRecipe, Recipe, Tag)
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import User
from users.serializers import UserSerializer


class IngredientinRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientinRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')
        extra_kwargs = {
            'id': {
                'read_only': False,
                'error_messages': {
                    'does_not_exist': 'Такого ингредиента не существует!'
                }
            }
        }
        validators = [
            UniqueTogetherValidator(
                queryset=IngredientinRecipe.objects.all(),
                fields=['ingredient', 'recipe']
            )
        ]


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects"""
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    """Serialize a recipe objects"""
    ingredients = IngredientinRecipeSerializer(source='ingredient_recipes',
                                               many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart', 'name',  'image',
                  'text',   'cooking_time')
        read_only_fields = ('id',)

    def validate(self, value):
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')
        ingredients_id = []
        if not ingredients:
            raise serializers.ValidationError('Нет ингредиентов')
        if not tags:
            raise serializers.ValidationError('Нет Тега')
        for ingredient in ingredients:
            if int(ingredient.get('amount')) <= 0:
                raise serializers.ValidationError(
                    ('Значение ингредиента не может быть меньше 0')
                )
        for ingredient in ingredients:
            ingredient = get_object_or_404(Ingredient,
                                           id=ingredient['id'])
            if ingredient in ingredients_id:
                raise serializers.ValidationError('Ингредиенты повторяются')
            ingredients_id.append(ingredient)
        value['ingredients'] = ingredients
        return value

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        image = validated_data.pop('image')
        recipe = Recipe.objects.create(image=image, **validated_data)
        tags = self.initial_data.get('tags')
        for tag in tags:
            recipe.tags.add(get_object_or_404(Tag, id=tag))
        for ingredient in ingredients:
            IngredientinRecipe.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount')
            )
        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        tags = self.initial_data.get('tags')
        instance.tags.set(tags)
        instance.ingredients.clear()
        ingredients = validated_data.get('ingredients')
        IngredientinRecipe.objects.filter(recipe=instance).all().delete()
        for ingredient in ingredients:
            ingredient_recipes = IngredientinRecipe.objects.create(
                recipe=instance,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount')
            )
            ingredient_recipes.save()
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                obj.favorite.get(user=user)
                return True
            except FavoriteRecipe.DoesNotExist:
                pass
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                obj.cart.get(user=user)
                return True
            except CartRecipe.DoesNotExist:
                pass
        return False


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        model = FavoriteRecipe
        fields = ('user', 'recipe')


class CartRecipeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        model = CartRecipe
        fields = ('user', 'recipe')
