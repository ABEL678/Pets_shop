from django.shortcuts import render

from catalog.models import Category, Product


def index(request):
    context = {
        'object_list': Category.objects.all(),
        'title': 'Pets shop - главная'
    }
    return render(request, 'catalog/index.html', context)


def categories(request):
    context = {
        'object_list': Category.objects.all(),
        'title': 'Каталог - наши товары'
    }
    return render(request, 'catalog/categories.html', context)


def category_product(request, pk):
    category_item = Category.objects.get(pk=pk)
    context = {
        'object_list': Product.objects.filter(category_id=pk),
        'title': f'товары в категории {category_item.category_name}'
    }
    return render(request, 'catalog/products.html', context)
