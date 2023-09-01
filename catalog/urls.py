from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import index, categories, category_product

app_name = CatalogConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('categories/', categories, name='categories'),
    path('<int:pk>/catalog', category_product, name='category_product'),
]
