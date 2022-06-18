from decimal import Decimal

from django.conf import settings
from ecommerce.apps.catalogue.models import Product
from ecommerce.apps.checkout.models import DeliveryOptions


class Basket:
    def __init__(self, request) -> None:
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def __iter__(self):
        """
        Collect the product id from session data to query database and return product/s
        """
        #  example of self.basket: {'2': {'price': '21.00', 'qty': 2}, '3': {'price': '19.99', 'qty': 1}}
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids).filter(is_active=True)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]["product"] = product

        for item in basket.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["qty"]
            yield item

    def __len__(self):
        """
        Get the basket total quantity
        """
        return sum([product["qty"] for product in self.basket.values()])

    def add(self, product, product_qty) -> None:
        product_id = str(product.id)
        if product_id in self.basket:
            self.basket[product_id]["qty"] = product_qty
        else:
            self.basket[product_id] = {"price": str(product.regular_price), "qty": product_qty}
        self.save()

    def delete(self, product_id) -> None:
        """
        Delete product from session data/basket
        """
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def update(self, product_id, product_qty):
        """
        Update product quantity in session data
        """
        if product_id in self.basket:
            self.basket[product_id]["qty"] = product_qty
        else:
            raise Exception("Something went wrong with product.")
        self.save()

    def get_subtotal_price(self):
        subtotal = Decimal(sum(Decimal(item["price"]) * int(item["qty"]) for item in self.basket.values()))
        return subtotal

    def get_total_price(self):
        total = self.get_subtotal_price()
        if "purchase" in self.session:
            delivery_price = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_option_id"]).price
            total += delivery_price
        return total

    def get_delivery_price(self):
        if "purchase" in self.session:
            return DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_option_id"]).price
        return 0

    def update_delivery(self, delivery_price=0):
        subtotal = self.get_subtotal_price()
        total = subtotal + Decimal(delivery_price)
        return total

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[settings.BASKET_SESSION_ID]
        del self.session["address"]
        del self.session["purchase"]
        self.save()
