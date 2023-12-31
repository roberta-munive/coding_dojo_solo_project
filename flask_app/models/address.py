from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import property, user, buyer
import re, datetime
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


class Address:
    db = "noteworthy_properties_schema" 
    def __init__(self, data):
        self.id = data['id']
        self.street = data['street']
        self.city = data['city']
        self.state = data['state']
        self.zipcode = data['zipcode']
        self.buyer_id = data['buyer_id']
        self.buyer_user_id = data['buyer_user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.buyer = None
        self.property_details = None
        self.realtor = None
        
    # Create Address Models

    # class method to save our address to the database
    @classmethod
    def create_address(cls, address_data):
        if not cls.validate_address(address_data):
            return False
        
        address_data = address_data.copy()

        query = """
                INSERT INTO addresses (street, city, state, zipcode, buyer_id, buyer_user_id) 
                VALUES (%(street)s, %(city)s, %(state)s, %(zipcode)s, %(buyer_id)s, %(buyer_user_id)s);
        """

        address_id = connectToMySQL(cls.db).query_db(query, address_data)

        return address_id
    
    # Read Address Models

    @classmethod
    def get_all_addresses_with_property_info_for_one_buyer(cls, buyer_id):

        data = {buyer_id: buyer_id}

        query = """
                SELECT * FROM buyers
                LEFT JOIN addresses 
                ON buyers.id = addresses.buyer_id
                LEFT JOIN properties
                ON properties.address_id = addresses.id
                WHERE address.buyer_id = %(buyer_id)s;
                """
        results = connectToMySQL(cls.db).query_db(query, data)
        all_addresses_with_properties = []
        for result in results:
            this_address = cls(result)
        
            this_address.buyer = buyer.Buyer({
                'id' : result['buyers.id'],
                'first_name' : result['first_name'],
                'last_name' : result['last_name'],
                'status' : result['buyers.status'],
                'user_id' : result['user_id'],
                'created_at' : result['buyers.created_at'],
                'updated_at' : result['buyers.updated_at']
            })
            this_address.property_details = property.Property({
                'id' : result['properties.id'],
                'status' : result['properties.status'],
                'client_ranking' : result['client_ranking'],
                'property_type' : result['property_type'],
                'year_constructed' : result['year_constructed'],
                'list_price' : result['list_price'],
                'positives' : result['positives'],
                'negatives' : result['negatives'],
                'address_id' : result['address_id'],
                'created_at' : result['properties.created_at'],
                'updated_at' : result['properties.updated_at']
            })
            all_addresses_with_properties.append(this_address)

        return all_addresses_with_properties
    
    @classmethod 
    def get_one_address_with_buyer_info(cls, address_id):

        data = {'id' : address_id}

        query = """
                SELECT * from addresses
                LEFT JOIN buyers 
                ON addresses.buyer_id = buyers.id 
                WHERE addresses.id = %(id)s;
                """
        results= connectToMySQL(cls.db).query_db(query, data)
        result = results[0]
        if result:
            this_address = cls(result)
            this_address.buyer=buyer.Buyer({
                'id': result['buyers.id'],
                'first_name' : result['first_name'],
                'last_name' : result['last_name'],
                'status' : result['status'],
                'created_at' : result['buyers.created_at'],
                'updated_at' : result['buyers.updated_at'],
                'user_id' : result['user_id']
            })
            
        return this_address
    
    @classmethod
    def get_one_address_with_property_and_buyer_info(cls, address_id):

        data = {'id' : address_id}

        query = """
                SELECT * from addresses
                LEFT JOIN buyers 
                ON addresses.buyer_id = buyers.id
                LEFT JOIN properties
                ON properties.address_id = addresses.id
                WHERE addresses.id = %(id)s;
                """
        results= connectToMySQL(cls.db).query_db(query, data)
        result = results[0]
        if result:
            this_address = cls(result)
            this_address.buyer=buyer.Buyer({
                'id': result['buyers.id'],
                'first_name' : result['first_name'],
                'last_name' : result['last_name'],
                'status' : result['status'],
                'created_at' : result['buyers.created_at'],
                'updated_at' : result['buyers.updated_at'],
                'user_id' : result['user_id']
            })

            this_address.property_details=property.Property({
                'id': result['properties.id'],
                'status' : result['properties.status'],
                'client_ranking' : result['client_ranking'],
                'property_type' : result['property_type'],
                'year_constructed' : result['year_constructed'],
                'list_price' : result['list_price'],
                'positives' : result['positives'],
                'negatives' : result['negatives'],
                'created_at' : result['properties.created_at'],
                'updated_at' : result['properties.updated_at'],
                'address_id' : result['address_id']
                
            })

        return this_address
    
    # the get_address_by_id method will be used when we need to retrieve just one specific row of the table
    @classmethod
    def get_address_by_id(cls, address_id):

        data = {'id': address_id}
        query = """
                SELECT * FROM addresses
                WHERE id = %(id)s;
        """
        
        results = connectToMySQL(cls.db).query_db(query, data)  # a list with one dictionary in it
        one_address = cls(results[0])
        return one_address # returns address object
    

    # Update Address Models

    

    # Delete Address Models

    @classmethod
    def delete_address(cls, address_id):
        this_address = cls.get_address_by_id(address_id)
        
        if session['user_id'] != this_address.buyer_user_id:
            return False
        
        data = {'id': address_id}

        query = """
                DELETE FROM addresses
                WHERE id = %(id)s;
        """
        
        return connectToMySQL(cls.db).query_db(query, data)
    
    
    # Validation

    @staticmethod
    def validate_address(address):

        is_valid = True
        if len(address['street']) < 1 or address['street'].isspace():
            flash("Street is required.", "error")
            is_valid = False
        if len(address['city']) < 1 or address['city'].isspace():
            flash("City is required.", "error")
            is_valid = False
        if len(address['state']) < 1 or address['state'].isspace():
            flash("State is required.", "error")
            is_valid = False
        if len(address['zipcode']) < 1 or address['zipcode'].isspace():
            flash("Zipcode is required.", "error")
            is_valid = False                          
        return is_valid
    
    