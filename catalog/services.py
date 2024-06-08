from django.core.cache import cache

from catalog.models import Category, Product
from config.settings import CACHE_ENABLED


def get_categories_from_cache():
    """Get categories from cache, if cache is empty, get categories from db"""
    if not CACHE_ENABLED:
        return Category.objects.all()
    key = 'categories_list'
    categories = cache.get(key)
    if categories is not None:
        return categories
    categories = Category.objects.all()
    cache.set(key, categories)
    return categories


def get_products_from_cache():
    """Get products from cache, if cache is empty, get products from db"""
    if not CACHE_ENABLED:
        return Product.objects.all()
    key = 'products_list'
    products = cache.get(key)
    if products is not None:
        return products
    products = Category.objects.all()
    cache.set(key, products)
    return products
