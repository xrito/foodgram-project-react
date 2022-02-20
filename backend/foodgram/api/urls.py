from cProfile import run

from django.urls import include, path
# from rest_framework.routers import SimpleRouter
from rest_framework import routers

from api.views import (IngredientinRecipeViewSet, IngredientViewSet,
                       RecipeViewSet, TagViewSet, UserViewSet, profile)

from .views import FavoriteRecipeList

router = routers.DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('inrecipe', IngredientinRecipeViewSet, basename='inrecipes')
router.register('users', UserViewSet)

urlpatterns = [
    path('v1/users/me/', profile, name='profile'),
    path('v1/', include(router.urls)),
    path('v1/favorites/', FavoriteRecipeList.as_view())
    # path('v1/auth/signup/', send_auth_code, name='send_auth_code'),
    # path('v1/auth/token/', get_token, name='get_access_token')
]
