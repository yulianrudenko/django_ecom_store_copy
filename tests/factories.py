import factory
from ecommerce.apps.catalogue.models import (
    Category,
    Product,
    ProductSpecification,
    ProductSpecificationValue,
    ProductType,
)
from faker import Faker

fake = Faker()

#############
# CATALOGUE #
#############
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ("name",)

    name = "django"
    slug = "django"


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType
        django_get_or_create = ("name",)

    name = "book"


class ProductSpecificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductSpecification

    product_type = factory.SubFactory(ProductTypeFactory)
    name = "pages"


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    product_type = factory.SubFactory(ProductTypeFactory)
    category = factory.SubFactory(CategoryFactory)
    title = "product_title"
    description = fake.text()
    slug = "product_slug"
    regular_price = "10.00"
    discount_price = "5.00"


class ProductSpecificationValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductSpecificationValue

    product = factory.SubFactory(ProductFactory)
    specification = factory.SubFactory(ProductSpecificationFactory)
    value = "100"
