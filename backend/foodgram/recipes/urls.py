from django.urls import path
from django.views.generic import TemplateView

app_name = 'recipes'

urlpatterns = [
    path('', TemplateView.as_view(template_name="recipes/index.html")),
]