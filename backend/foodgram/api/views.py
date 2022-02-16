from recipes.models import *
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer
from rest_framework import generics


class RecipeListCreate(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
