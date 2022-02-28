from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import *
from users.models import *
from rest_framework import filters, generics, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from users.serializers import SubscribeSerializer

from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer
from users.serializers import SubscribeSerializer
#  UserSerializer
User = get_user_model()


class ListCreateDeleteViewSet(mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    pass


# class UserViewSet(viewsets.ModelViewSet):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#     pagination_class = PageNumberPagination

#     @action(methods=['get'], detail=False)
#     def subscriptions(self, request):
#         users = User.objects.filter(is_subscribed=True)
#         return Response({'user': [c.username for c in users]})

    # @api_view(['GET'])
    # @permission_classes([permissions.AllowAny])

    # @action(methods=['get'], detail=False)
    # def me(self, request):
    #     if not request.user.is_authenticated:
    #         return Response('Not authorized', status=status.HTTP_401_UNAUTHORIZED)
    #     if request.method == 'GET':
    #         serializer = ProfileSerializer(request.user)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     serializer = ProfileSerializer(request.user, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = PageNumberPagination


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = PageNumberPagination
    search_fields = ('^name',)
    filter_backends = [DjangoFilterBackend]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tags__slug']

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk):
        favorite = FavoriteRecipe.objects.all().filter(
            recipe_id=pk, user_id=self.request.user.id)
        if request.method == 'POST':
            favorite = FavoriteRecipe.objects.create(
                recipe_id=pk, user_id=self.request.user.id)
            favorite.save()
            return Response({"message": "Favorite Created Successfully"}, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            favorite.delete()
            return Response({"message": "Favorite Deleted"}, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['get', 'delete'])
    def shopping_cart(self, request, pk=None):
        if request.method == 'GET':
            return self.add_obj(CartRecipe, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_obj(CartRecipe, request.user, pk)
        return None


# class IngredientinRecipeViewSet(viewsets.ModelViewSet):
#     queryset = IngredientinRecipe.objects.all()
#     serializer_class = IngredientinRecipeSerializer
#     pagination_class = PageNumberPagination

# class FavoriteRecipeList(generics.ListAPIView):
#     """List all the the Favorites"""
#     serializer_class = FavoriteRecipeSerializer
#     pagination_class = PageNumberPagination

#     def get_queryset(self):
#         queryset = FavoriteRecipe.objects.filter(user=self.request.user)
#         return queryset


# class FavoriteRecipeViewSet(viewsets.ModelViewSet):
#     """List all the the Favorites"""
#     # queryset = FavoriteRecipe.objects.all()
#     serializer_class = FavoriteRecipeSerializer
#     pagination_class = PageNumberPagination

#     def get_queryset(self):
#         # queryset = FavoriteRecipe.objects.filter(user=self.request.user)
#         # return queryset
#         # recipe_id = get_object_or_404(FavoriteRecipe, id=self.kwargs.get('recipe_id'))
#         # return recipe_id.favorites.all()
#         user_id = get_object_or_404(User, pk=self.request.user.pk)
#         queryset = user_id.favorite.all()
#         return queryset


class CreateRetrieveViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    pass


class SubscribeViewSet(CreateRetrieveViewSet):
    queryset =Subscription.objects.all()
    serializer_class = SubscribeSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__username', 'subscribing__username')
    pagination_class = PageNumberPagination
    # permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)

    def get_queryset(self):
        user_id = get_object_or_404(User, pk=self.request.user.pk)
        queryset = user_id.subscriber.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
