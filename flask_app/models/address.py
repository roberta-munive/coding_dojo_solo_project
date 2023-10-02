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
        self.property = None
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
        # one_buyer = buyer.Buyer.get_buyer_by_id(buyer_id)
        # query = """
        #         SELECT * FROM properties
        #         LEFT JOIN addresses
        #         ON properties.address_id = addresses.id
        #         WHERE properties.buyer_id = buyer_id;
        #         """
        query = """
                SELECT * FROM buyers
                LEFT JOIN addresses 
                ON buyers.id = addresses.buyer_id
                LEFT JOIN properties
                ON properties.address_id = addresses.id
                WHERE addresses.buyer_id = buyer_id;
                """
        results = connectToMySQL(cls.db).query_db(query)
        all_addresses_with_properties = []
        for result in results:
            this_address = cls(result)
            # this_address.buyer = one_buyer
            this_address.buyer = buyer.Buyer({
                'id' : result['buyers.id'],
                'first_name' : result['first_name'],
                'last_name' : result['last_name'],
                'status' : result['buyers.status'],
                'user_id' : result['user_id'],
                'created_at' : result['buyers.created_at'],
                'updated_at' : result['buyers.updated_at']
            })
            this_address.property = property.Property({
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
    def get_all_addresses_for_one_buyer(cls, buyer_id):
        query = """
                SELECT * FROM addresses
                WHERE addresses.buyer_id = buyer_id;
                """
        results = connectToMySQL(cls.db).query_db(query)
        all_addresses_for_one_buyer = []
        for result in results:
            this_address = cls(result)
            all_addresses_for_one_buyer.append(this_address)
        return all_addresses_for_one_buyer
    
    # @classmethod
    # def get_all_cars_and_users(cls):
    #     query = """
    #             SELECT * FROM cars
    #             LEFT JOIN users
    #             ON cars.user_id = users.id;
    #             """
    #     results = connectToMySQL(cls.db).query_db(query)
    #     all_cars_with_users = []
    #     for result in results:
    #         this_car = cls(result)
    #         this_car.owner = user.User({
    #             'id' : result['users.id'],
    #             'first_name' : result['first_name'],
    #             'last_name' : result['last_name'],
    #             'email' : result['email'],
    #             'password' : result['password'],
    #             'created_at' : result['users.created_at'],
    #             'updated_at' : result['users.updated_at']
    #         })
    #         all_cars_with_users.append(this_car)
    #     return all_cars_with_users


    # # the get_address_by_id method will be used when we need to retrieve just one specific row of the table
    @classmethod
    def get_address_by_id(cls, id):
        query = """
                SELECT * FROM addresses
                WHERE id = %(id)s;
        """
        data = {'id': id}
        results = connectToMySQL(cls.db).query_db(query, data)  # a list with one dictionary in it
        one_address = cls(results[0])
        return one_address # returns address object
    
    # @classmethod
    # def get_car_by_id_with_user(cls, id):
    #     query = """
    #             SELECT * FROM cars
    #             LEFT JOIN users
    #             ON cars.user_id = users.id
    #             WHERE cars.id = %(id)s;
    #             """
    #     data = {'id': id}
    #     results = connectToMySQL(cls.db).query_db(query, data)  # a list with one dictionary in it
    #     one_car=results[0] # one dictionary
    #     return one_car # returns address dictionary


    # # Update Address Models

    # @classmethod
    # def update_car(cls, data):  

    #     this_car = cls.get_car_by_id(data['id'])
    #     if session['user_id'] != this_car.user_id:
    #         return False
        
    #     is_valid = cls.validate_car(data)

    #     if not is_valid:
    #         return False
        
        
    #     query = """
    #             UPDATE cars
    #             SET price = %(price)s,
    #                 model = %(model)s,
    #                 make = %(make)s,
    #                 year = %(year)s,
    #                 description = %(description)s
    #             WHERE id=%(id)s;    
    #     """
    #     connectToMySQL(cls.db).query_db(query, data)
    #     return True
    

    # # Delete Car Models

    # @classmethod
    # def delete_car(cls, id):
    #     this_car = cls.get_car_by_id(id)
        
    #     if session['user_id'] != this_car.user_id:
    #         return False
        
    #     query = """
    #             DELETE FROM cars
    #             WHERE id = %(id)s;
    #     """
    #     data = {'id': id}
    #     return connectToMySQL(cls.db).query_db(query, data)
    
    # @classmethod
    # def purchase_car(cls, id):
    #     this_car = cls.get_car_by_id(id)
        
    #     query = """
    #             DELETE FROM cars
    #             WHERE id = %(id)s;
    #     """
    #     data = {'id': id}
    #     return connectToMySQL(cls.db).query_db(query, data)
    
    # # Validation      

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
    
    