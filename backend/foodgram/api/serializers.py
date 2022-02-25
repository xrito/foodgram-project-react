from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (CartRecipe, FavoriteRecipe, Ingredient,
                            IngredientinRecipe, Recipe, Tag)
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r"^[\w.@+-]+\Z", required=True, max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True, max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(required=False, max_length=150)
    last_name = serializers.CharField(required=False, max_length=150)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')
        lookup_field = 'id'


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r"^[\w.@+-]+\Z", required=False, max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=False, max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(required=False, max_length=150)
    last_name = serializers.CharField(required=False, max_length=150)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')


class IngredientinRecipeSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientinRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')
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
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects"""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', )


class RecipeListSerializer(serializers.ModelSerializer):
    """Serialize a recipe"""
    ingredients = IngredientinRecipeSerializer(many=True, read_only=True)
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
        extra_kwargs = {'ingredients': {'required': False}}

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

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
    user = UserSerializer(read_only=True)
    recipe = RecipeListSerializer(read_only=True)

    class Meta:
        model = FavoriteRecipe
        fields = ('id', 'user', 'recipe')
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }
