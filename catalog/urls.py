from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import contacts, IndexView, ProductDetailView, blog_list_view, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, categories

app_name = CatalogConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contacts/', contacts),
    path('product/<int:product_id>/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete'),
    path('category/', categories, name='category_list'),
    path('list/', blog_list_view, name='blog_list'),
]
