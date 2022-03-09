from djoser.serializers import \
    UserCreateSerializer as BaseUserRegistrationSerializer
from recipes.models import Recipe
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import Subscription, User


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password')


class SubscribeRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes')
        lookup_field = 'id'

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                obj.subscribing.get(user=user)
                return True
            except Subscription.DoesNotExist:
                pass
        return False

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj.id)
        return SubscribeRecipeSerializer(queryset, many=True).data


class SubscribeSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='subscribing.email')
    id = serializers.ReadOnlyField(source='subscribing.id')
    username = serializers.ReadOnlyField(source='subscribing.username')
    first_name = serializers.ReadOnlyField(source='subscribing.first_name')
    last_name = serializers.ReadOnlyField(source='subscribing.last_name')
    is_subscribed = serializers.ReadOnlyField(default=True)
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.subscribing).count()

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj.subscribing)
        return SubscribeRecipeSerializer(queryset, many=True).data

    validators = [
        UniqueTogetherValidator(
            queryset=Subscription.objects.all(),
            fields=('user', 'subscribing')
        )
    ]

    def validate(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!')
