
from pprint import pprint

import unicodecsv as csv
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import *
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from users.models import *
from users.serializers import SubscribeSerializer, UserSerializer

from .filters import RecipesFilter
from .serializers import (FavoriteRecipeSerializer, IngredientSerializer,
                          RecipeSerializer, TagSerializer)


class ListCreateDeleteViewSet(mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    pass


class UserViewSet(UserViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = PageNumberPagination

    @action(methods=['get'], detail=False)
    def subscriptions(self, serializer):
        queryset = Subscription.objects.filter(user=self.request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, id):
        queryset = Subscription.objects.all().filter(
            subscribing_id=id, user_id=self.request.user.id)
        if request.method == 'POST':
            queryset = Subscription.objects.create(
                subscribing_id=id, user_id=self.request.user.id)
            queryset.save()
            return Response({"message": "Subscription Created Successfully"}, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            queryset.delete()
            return Response({"message": "Unsubscribed"}, status=status.HTTP_202_ACCEPTED)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = PageNumberPagination
    # permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('^name',)
    filter_backends = [DjangoFilterBackend]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    # permission_classes = [IsOwnerOrReadOnly]
    filterset_class = RecipesFilter

    @action(methods=['get'], detail=False)
    def favorites(self, serializer):
        queryset = FavoriteRecipe.objects.filter(user=self.request.user)
        page = self.paginate_queryset(queryset)
        serializer = FavoriteRecipeSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk):
        favorite = FavoriteRecipe.objects.all().filter(
            recipe_id=pk, user_id=self.request.user.id)
        if request.method == 'POST':
            favorite = FavoriteRecipe.objects.create(
                recipe_id=pk, user_id=self.request.user.id)
            favorite.save()
            return Response({"message": "Recipe added to favorites"}, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            favorite.delete()
            return Response({"message": "Recipe removed from favorites"}, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk=None):
        cart = CartRecipe.objects.all().filter(
            recipe_id=pk, user_id=self.request.user.id)
        if request.method == 'POST':
            cart = CartRecipe.objects.create(
                recipe_id=pk, user_id=self.request.user.id)
            cart.save()
            return Response({"message": "Recipe added to cart"}, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            cart.delete()
            return Response({"message": "Recipe removed from cart"}, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['GET'])
    def download_shopping_cart(self, request):
        """Generate TXT file CartRecipe List"""
        response = HttpResponse(content_type='text/plain; charset=UTF-8')
        response['Content-Disposition'] = 'attachment; filename=shopping_cart.txt'
        carts = CartRecipe.objects.all().filter(user_id=self.request.user.id)
        lst = {}
        for cart in carts:
            recipe = cart.recipe
            ingredients = IngredientinRecipe.objects.filter(recipe=recipe).values(
                'ingredient__name', 'ingredient__measurement_unit', 'amount')
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
            [f'{key.capitalize()}: {" ".join(map(str,list(value.values())))}\n' for key, value in lst.items()])
        response.writelines(result)
        return response
