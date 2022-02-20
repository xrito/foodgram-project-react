from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from recipes.models import *
from rest_framework import filters, mixins, status, viewsets, generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .serializers import (IngredientinRecipeSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeListSerializer,
                          TagSerializer, UserSerializer, ProfileSerializer, FavoriteRecipeSerializer)

User = get_user_model()


class ListCreateDeleteViewSet(mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    pass


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

    @action(methods=['get'], detail=False)
    def subscriptions(self, request):
        users = User.objects.filter(is_subscribed=True)
        return Response({'user': [c.username for c in users]})


@api_view(['GET'])
# @permission_classes([permissions.AllowAny])
def profile(request):
    if not request.user.is_authenticated:
        return Response('Not authorized', status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'GET':
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    serializer = ProfileSerializer(request.user, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.OrderingFilter]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer
    pagination_class = PageNumberPagination

    # @action(methods=['get'], detail=False)
    # def tag(self, request):
    #     tags = Tag.objects.all()
    #     return Response({'tags': [c.name for c in tags]})

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk):
        favorite = FavoriteRecipe.objects.all().filter(
            recipe_id=pk, user_id=self.request.user.id)
        if request.method == 'POST':
            if Recipe.objects.filter(is_favorited__in=["True"]):
                favorite = FavoriteRecipe.objects.create(
                    recipe_id=pk, user_id=self.request.user.id)
                favorite.save()
                return Response({"message": "Favorite Created Successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Favorite is Already Created"}, status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            if Recipe.objects.filter(is_favorited__in=["True"]):
                favorite.delete()
                return Response({"message": "Favorite Deleted"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"error": "Favorite is Already Deleted"}, status=status.HTTP_400_BAD_REQUEST)


class IngredientinRecipeViewSet(viewsets.ModelViewSet):
    queryset = IngredientinRecipe.objects.all()
    serializer_class = IngredientinRecipeSerializer


class FavoriteRecipeList(generics.ListAPIView):
    """List all the the Favorites"""
    serializer_class = FavoriteRecipeSerializer
    queryset = FavoriteRecipe.objects.all()
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = FavoriteRecipe.objects.filter(user=self.request.user)
        return queryset
