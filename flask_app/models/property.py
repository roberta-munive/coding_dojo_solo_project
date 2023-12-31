from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user, buyer, address
import re, datetime
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


class Property:
    db = "noteworthy_properties_schema" 
    def __init__(self, data):
        self.id = data['id']
        self.status = data['status']
        self.client_ranking = data['client_ranking']
        self.property_type = data['property_type']
        self.year_constructed = data['year_constructed']
        self.list_price = data['list_price']
        self.positives = data['positives']
        self.negatives = data['negatives']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.address_id = data['address_id']
        self.this_address = None 
        
    # Create Property Models

    # class method to save our property to the database
    @classmethod
    def create_property(cls, property_data):
        if not cls.validate_property(property_data):
            return False
        
        property_data = property_data.copy()

        query = """
                INSERT INTO properties (status, client_ranking, property_type, year_constructed, list_price, positives, negatives, address_id) 
                VALUES (%(status)s, %(client_ranking)s, %(property_type)s, %(year_constructed)s, %(list_price)s, %(positives)s, %(negatives)s, %(address_id)s);
                """

        property_id = connectToMySQL(cls.db).query_db(query, property_data)

        return property_id

    # Read Property Models



    # Update Property Models

    @classmethod
    def update_property(cls, property_data):  

        property_data = property_data.copy()

        this_address = address.Address.get_address_by_id(property_data['address_id'])

        if session['user_id'] != this_address.buyer_user_id:
            return False
        
        is_valid = cls.validate_property(property_data)

        if not is_valid:
            return False
        
        query = """
                UPDATE properties
                SET status = %(status)s,
                    client_ranking = %(client_ranking)s,
                    property_type = %(property_type)s,
                    year_constructed = %(year_constructed)s,
                    list_price = %(list_price)s,
                    positives = %(positives)s,
                    negatives = %(negatives)s
                WHERE id=%(id)s;    
                """
        connectToMySQL(cls.db).query_db(query, property_data)
        return True
    

    # Delete Car Models

    
    # Validation      

    @staticmethod
    def validate_property(property):

        is_valid = True
        if len(property['status']) < 1 or property['status'].isspace():
            flash("Property status is required.", "error")
            is_valid = False
        if len(property['client_ranking']) < 1 or property['client_ranking'].isspace():
            flash("Client ranking is required. Use 0 for undecided.", "error")
            is_valid = False    
        elif int(property['client_ranking']) < 0:
            flash("Client ranking cannot be negative. Use 0 for undecided.", "error")
            is_valid = False    
        if len(property['property_type']) < 1 or property['property_type'].isspace():
            flash("Property type is required.", "error")
            is_valid = False
        if len(property['year_constructed']) < 1 or property['year_constructed'].isspace():
            flash("Year constructed is required.", "error")
            is_valid = False   
        if len(property['list_price']) < 1 or property['list_price'].isspace():
            flash("Property price is required.", "error")
            is_valid = False    
        elif int(property['list_price']) < 1:
            flash("Property price must be greater than $0.", "error")
            is_valid = False
        if len(property['positives']) < 1 or property['positives'].isspace():
            flash("Positives are required.", "error")
            is_valid = False
        if len(property['negatives']) < 1 or property['negatives'].isspace():
            flash("Negatives are required.", "error")
            is_valid = False                         
        return is_valid
    
    