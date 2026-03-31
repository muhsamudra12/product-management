import os
import logging
import unittest
from flask_api import status
from service import app
from service.models import db, Product
from tests.factories import ProductFactory

DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///test.db")
BASE_URL = "/products"

class TestProductRoutes(unittest.TestCase):
    """Test Cases for Product Routes"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        # Setup context so that the db can be accessed at the class level
        cls.app_context = app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()
        cls.app_context.pop()

    def setUp(self):
        """Runs before each test"""
        db.drop_all()
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        """Runs after each test"""
        db.session.remove()

    ##################################################
    # TEST CASES
    ##################################################

    def test_get_product(self):
        """It should Read a single Product"""
        test_product = ProductFactory()
        resp = self.client.post(BASE_URL, json=test_product.serialize(), content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
        new_product = resp.get_json()
        resp = self.client.get(f"{BASE_URL}/{new_product['id']}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], test_product.name)

    def test_get_product_not_found(self):
        """It should not Find a Product that is not found"""
        resp = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_query_product_list_by_category(self):
        """It should List Products by Category"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        
        category = products[0].category
        resp = self.client.get(BASE_URL, query_string=f"category={category}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len([p for p in products if p.category == category]))
        for product in data:
            self.assertEqual(product["category"], category)