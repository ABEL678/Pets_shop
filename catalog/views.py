from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from blog.models import Blog
from catalog.models import Product, Category, Version
from catalog.forms import ProductForm, VersionForm

from django.shortcuts import get_object_or_404, render
from django.views import View

from catalog.services import get_categories_cache
from config import settings


@login_required
def categories(request):

    context = {
        'object_list': get_categories_cache(),
        'title': 'Каталог - наши товары'
    }
    return render(request, 'catalog/category_list.html', context)


class IndexView(ListView):
    template_name = 'catalog/index.html'
    model = Product

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff or user.is_superuser:
                queryset = super().get_queryset()
            else:
                queryset = super().get_queryset().filter(
                    status=Product.STATUS_PUBLISH
                )
        else:
            queryset = super().get_queryset().filter(
                status=Product.STATUS_PUBLISH
            )
        return queryset


# class CategoryListView(ListView):
#     template_name = 'catalog/category_list.html'
#     model = Category
#     extra_context = {
#         'title': 'Каталог - наши товары'
#     }


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(category_id=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        category_item = Category.objects.get(pk=self.kwargs.get('pk'))
        context_data['category_pk'] = category_item.pk,
        context_data['title'] = f'товары в категории {category_item.category_name}'

        return context_data


class ProductDetailView(View):
    template_name = 'catalog/product_detail.html'

    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        return render(request, self.template_name, {'product': product})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('index')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} ({email}): {message}')
    return render(request, 'catalog/contacts.html')


def blog_list_view(request):
    blogs = Blog.objects.all()
    return render(request, 'blog/list.html', {'blogs': blogs})


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('index')
    permission_required = 'catalog.change_product'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            formset = VersionFormset(self.request.POST, instance=self.object)
        else:
            formset = VersionFormset(instance=self.object)

        context_data['formset'] = formset

        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

    def test_func(self):
        user = self.request.user
        product = self.get_object()

        if product.owner == user or user.is_staff:
            return True
        return False

    def handle_no_permission(self):
        return redirect(reverse_lazy('index'))
