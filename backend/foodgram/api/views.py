from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from .filters import IngredientFilter, RecipesFilter
from .pagination import PageLimitPagination
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (FavoriteRecipeSerializer, IngredientSerializer,
                          RecipeSerializer, TagSerializer)
from recipes.models import (CartRecipe, FavoriteRecipe, Ingredient,
                            IngredientinRecipe, Recipe, Tag)
from users.models import Subscription, User
from users.serializers import SubscribeSerializer, UserSerializer


class UserViewSet(UserViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = PageLimitPagination
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated])
    def subscriptions(self, serializer):
        queryset = Subscription.objects.filter(user=self.request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id):
        if request.method == 'POST':
            subscribing = get_object_or_404(User, id=id)
            if request.user == subscribing:
                return Response(
                    {"errors": "Нельзя подписаться на самого себя!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                queryset = Subscription.objects.create(
                    subscribing_id=id, user_id=self.request.user.id)
                queryset.save()
                return Response({"errors": "Подписка успешно создана."},
                                status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"errors": "Повторная подписка невозможна."},
                                status=status.HTTP_400_BAD_REQUEST,
                                )
        if request.method == 'DELETE':
            queryset = Subscription.objects.get(
                subscribing_id=id, user_id=self.request.user.id)
            try:
                queryset.delete()
            except ObjectDoesNotExist:
                return Response(
                    {"errors": "Подписка не найдена."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ('^name',)
    filter_backends = [DjangoFilterBackend]
    filter_class = IngredientFilter


class MyMixin:
    def object_post(self, model, user, pk):
        try:
            model.objects.create(user=user, recipe_id=pk)
            return Response(status=status.HTTP_201_CREATED)
        except Exception:
            if model.objects.filter(user=user, recipe__id=pk).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)

    def object_delete(self, model, user, pk):
        try:
            model.objects.get(user=user, recipe_id=pk).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RecipeViewSet(MyMixin, ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageLimitPagination
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthorOrReadOnly]
    filterset_class = RecipesFilter

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated])
    def favorites(self, serializer):
        queryset = FavoriteRecipe.objects.filter(user=self.request.user)
        page = self.paginate_queryset(queryset)
        serializer = FavoriteRecipeSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['post', 'delete'],
            detail=True, permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self.object_post(FavoriteRecipe, self.request.user, pk)
        if request.method == 'DELETE':
            return self.object_delete(FavoriteRecipe, self.request.user, pk)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self.object_post(CartRecipe, self.request.user, pk)
        if request.method == 'DELETE':
            return self.object_delete(CartRecipe, self.request.user, pk)

    @action(detail=False, methods=['GET'])
    def download_shopping_cart(self, request):
        """Generate TXT file CartRecipe List"""
        response = HttpResponse(content_type='text/plain; charset=UTF-8')
        response['Content-Disposition'] = (
            'attachment; filename=shopping_cart.txt')
        carts = CartRecipe.objects.all().filter(user_id=self.request.user.id)
        lst = {}
        for cart in carts:
            recipe = cart.recipe
            ingredients = (IngredientinRecipe.objects.filter(recipe=recipe)
                           .values('ingredient__name',
                                   'ingredient__measurement_unit', 'amount'))
            for ingredient in ingredients:
                name = ingredient['ingredient__name']
                measurement_unit = ingredient['ingredient__measurement_unit']
                amount = ingredient['amount']
                if name not in lst:
                    lst[name] = {
                        'measurement_unit': measurement_unit,
                        'amount': amount
                    }
                else:
                    lst[name]['amount'] += amount
        result = ''.join(
            [f'{key.capitalize()}: {" ".join(map(str,list(value.values())))}\n'
             for key, value in lst.items()])
        response.writelines(result)
        return response
