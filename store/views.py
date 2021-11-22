from django.shortcuts import render, get_list_or_404
from .models import Category, Product

""" Display the Product Categories """


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    # if category slug exists
    if category_slug:
        # category is assigned the list of all categories
        category = get_list_or_404(Category, slug=category_slug)
        # return optional products by a product filter
        products = products.filter(category=category)
    return render(request, 'store/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


""" Display a single Product """


def product_detail(request, id, slug):
    # product takes a id & slug (must be available)
    product = get_list_or_404(Product,
                              id=id,
                              slug=slug,
                              available=True)
    return render(request, 'store/product/detail.html',
                  {'product': product})
