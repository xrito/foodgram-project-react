from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (CartRecipe, FavoriteRecipe, Ingredient,
                            IngredientinRecipe, Recipe, Subscribe, Tag)
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
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
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.StringRelatedField(many=True, read_only=True)


    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes')
        lookup_field = 'id'

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                obj.subscribed.get(user=user)
                return True
            except Subscribe.DoesNotExist:
                pass
        return False


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


class RecipeSerializer(serializers.ModelSerializer):
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
    recipe = RecipeSerializer(read_only=True)

    class Meta:
        model = FavoriteRecipe
        fields = ('id', 'user', 'recipe')
        # extra_kwargs = {
        #     'id': {
        #         'read_only': True
        #     }
        # }


class SubscribeSerializer(serializers.ModelSerializer):
    # user = serializers.CharField(
    #     read_only=True, default=serializers.CurrentUserDefault()
    # )
    # subscribed = serializers.SlugRelatedField(
    #     slug_field='username',
    #     queryset=User.objects.all(),
    # )
    subscribed = UserSerializer(read_only=True)
    class Meta:
        model = Subscribe
        fields = ('subscribed',)
    #     validators = [
    #         UniqueTogetherValidator(
    #             queryset=Subscribe.objects.all(),
    #             fields=('user', 'subscribed')
    #         )
    #     ]

    # def validate_following(self, value):
    #     if value == self.context['request'].user:
    #         raise serializers.ValidationError(
    #             'Нельзя подписаться на самого себя!')
    #     return value
