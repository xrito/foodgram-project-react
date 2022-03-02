from django.urls import include, path
from rest_framework import routers

from api.views import (IngredientViewSet, RecipeViewSet, 
                       TagViewSet, UserViewSet)

# UserViewSet,
router = routers.DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('users', UserViewSet, basename='users')
# router.register('inrecipe', IngredientinRecipeViewSet, basename='inrecipes')
# router.register('favorites', FavoriteRecipeViewSet, basename='favorites')
# router.register('users/subscriptions', SubscribeViewSet,
#                 basename='subscriptions')
# router.register(
#     r'users/(?P<author_id>\d+)/subscribe', SubscribeViewSet, basename='subscribe')
# router.register('users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
