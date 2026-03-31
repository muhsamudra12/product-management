from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
from service import db

class DataValidationError(Exception):
    """Used for data validation errors when deserializing"""

class Product(db.Model):
    """
    Class that represents a Product
    """
    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256))
    price = db.Column(db.Numeric(10, 2), nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=True)
    category = db.Column(db.String(64))

    def __repr__(self):
        return f"<Product {self.name} id=[{self.id}]>"

    def create(self):
        """Creates a Product to the database"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates a Product to the database"""
        if not self.id:
            raise DataValidationError("Update called on object without ID")
        db.session.commit()

    def delete(self):
        """Removes a Product from the data store"""
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes a Product into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": str(self.price), # Decimal to string for JSON
            "available": self.available,
            "category": self.category
        }

    def deserialize(self, data):
        """Deserializes a Product from a dictionary"""
        try:
            self.name = data["name"]
            self.description = data["description"]
            self.price = data["price"]
            self.available = data["available"]
            self.category = data["category"]
        except KeyError as error:
            raise DataValidationError("Invalid Product: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError("Invalid Product: body of request contained bad or no data")
        return self

    ##################################################
    # CLASS METHODS (Query Helpers for Task 2)
    ##################################################

    @classmethod
    def all(cls):
        """Returns all Products in the database"""
        return cls.query.all()

    @classmethod
    def find(cls, product_id):
        """Finds a Product by its ID"""
        return cls.query.get(product_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Products with the given name"""
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_category(cls, category):
        """Returns all Products in a specific category"""
        return cls.query.filter(cls.category == category)

    @classmethod
    def find_by_availability(cls, available=True):
        """Returns all Products by their availability"""
        return cls.query.filter(cls.available == available)
    
    @classmethod
    def init_db(cls, app):
        """Initializes the database"""
        db.init_app(app)