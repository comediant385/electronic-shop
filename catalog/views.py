from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm, ProductModeratorForm
from catalog.models import Product, Version, Category
from catalog.services import get_products_from_cache, get_categories_from_cache


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        products = Product.objects.all()
        for product in products:
            versions = Version.objects.filter(product=product)
            active_versions = versions.filter(version_current_sign=True)
            if active_versions:
                product.active_version = active_versions.last().version_name
                product.active_version_number = active_versions.last().version_number
            else:
                product.active_version = "-"
                product.active_version_number = "-"
        context_data['object_list'] = products
        return context_data

    def get_queryset(self):
        return get_products_from_cache()


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        if form.is_valid:
            new_object = form.save(commit=False)
            new_object.author = self.request.user
            new_object.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:home")

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_form_class(self):
        user = self.request.user
        if user == self.object.user:
            return ProductForm
        if (user.has_perm('catalog.can_cancel_puplication') and
                user.has_perm('catalog.can_change_desription') and user.has_perm('catalog.can_change_category')):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:home")


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            message = request.POST.get("message")
            print(f"Message from {name} (Tel: {phone}): {message}")
        return render(request, self.template_name)


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "catalog/category_list.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context_data['category_list'] = categories
        return context_data

    def get_queryset(self):
        return get_categories_from_cache()