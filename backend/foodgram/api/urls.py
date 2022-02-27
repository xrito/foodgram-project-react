from cProfile import run

from django.urls import include, path
# from rest_framework.routers import SimpleRouter
from rest_framework import routers

from api.views import (IngredientinRecipeViewSet, IngredientViewSet,
                       RecipeViewSet, TagViewSet, UserViewSet, FavoriteRecipeViewSet, SubscribeViewSet) # profile

# from .views import FavoriteRecipeList

router = routers.DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('inrecipe', IngredientinRecipeViewSet, basename='inrecipes')
router.register('users', UserViewSet, basename='users')
router.register('favorites', FavoriteRecipeViewSet, basename='favorites')
router.register('subscriptions', SubscribeViewSet, basename='subscriptions')


urlpatterns = [
    # path('users/me/', profile, name='profile'),
    path('', include(router.urls)),
    # path('favorites/', FavoriteRecipeList.as_view())
    # path('v1/auth/signup/', send_auth_code, name='send_auth_code'),
    # path('v1/auth/token/', get_token, name='get_access_token')
]
