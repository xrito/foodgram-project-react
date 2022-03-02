from django_filters import rest_framework
from django_filters.filters import CharFilter

from recipes.models import Recipe


class RecipesFilter(rest_framework.FilterSet):
    tags = CharFilter(field_name='tags__slug',)

    class Meta:
        model = Recipe
        fields = ('tags',)
