from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (RecipeListCreate)

router = SimpleRouter()
router.register('recipes', RecipeListCreate.as_view(), basename='recipes')



urlpatterns = [
    # path('v1/users/me/', profile, name='profile'),
    path('v1/recipes', RecipeListCreate.as_view()),
    # path('v1/auth/signup/', send_auth_code, name='send_auth_code'),
    # path('v1/auth/token/', get_token, name='get_access_token')
]
