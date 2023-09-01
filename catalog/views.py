from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from catalog.models import Category, Product
from blog.models import Blog
from catalog.models import Product, Version
from catalog.forms import ProductForm, VersionForm

from django.shortcuts import get_object_or_404, render
from django.views import View


def index(request):
    context = {
        'object_list': Category.objects.all(),
        'title': 'Pets shop - главная'
    }
    return render(request, 'catalog/index.html', context)


class CategoryListView(ListView):
    model = Category
    extra_context = {
        'title': 'Каталог - наши товары'
    }


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


class ProductCreateView(CreateView):
    model = Product
    fields = ('product_name', 'category',)
    success_url = reverse_lazy('catalog:categories')


class ProductDetailView(View):
    template_name = 'catalog/product_detail.html'

    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        return render(request, self.template_name, {'product': product})


class ProductDeleteView(DeleteView):
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


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('index')

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