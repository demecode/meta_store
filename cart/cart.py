from decimal import Decimal
from django.conf import settings
from myshop.store.models import Product


class Cart(object):
    def __init__(self, request):
        """ lets initialize the cart """

        # lets store the current session here
        self.session = request.session

        # get the cart session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # if no cart, save an empty car in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
            self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """ lets add a product using the product instance, or update the quantity """
        # get product id
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        """ mark the session as modified as verification the session has been saved """
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """ in order to find the products to remove / add we need to iterate over the cart """

        product_ids = self.cart.keys()
        # get product objects & add to cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """ gotsa count all them items in the cart """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """ remove current cart from session """
        del self.session[settings.CART_SESSION_ID]
        self.save()
