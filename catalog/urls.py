from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import contacts, index, ProductDetailView, blog_list_view, ProductCreateView, ProductUpdateView, \
    ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('contacts/', contacts),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete'),
    path('list/', blog_list_view, name='catalog_list'),
]
