import factory
from factory import fuzzy
from service.models import Product

class ProductFactory(factory.Factory):
    """Creates fake products for testing"""
    class Meta:
        model = Product

    id = factory.Sequence(lambda n: n)
    name = fuzzy.FuzzyChoice(choices=["Laptop", "Smartphone", "Headphones", "Monitor"])
    description = factory.Faker("text")
    price = fuzzy.FuzzyDecimal(10.0, 1000.0, 2)
    available = fuzzy.FuzzyChoice(choices=[True, False])
    category = fuzzy.FuzzyChoice(choices=["Electronics", "Apparel", "Home Supplies"])