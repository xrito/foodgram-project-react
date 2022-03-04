from django_filters.rest_framework import FilterSet, filters
from recipes.models import Recipe
from users.models import User

class RecipesFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(method='filter_is_favorited', lookup_expr='isnull', exclude=True)
    # is_in_shopping_cart = filters.BooleanFilter(method='filter_is_in_shopping_cart', lookup_expr='isnull')
    
    def filter_is_favorited(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('tags','author','is_favorited')
