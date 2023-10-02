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
        self.address = None 
        
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


    # # the get_property_by_id method will be used when we need to retrieve just one specific row of the table
    # @classmethod
    # def get_car_by_id(cls, id):
    #     query = """
    #             SELECT * FROM cars
    #             WHERE id = %(id)s;
    #     """
    #     data = {'id': id}
    #     results = connectToMySQL(cls.db).query_db(query, data)  # a list with one dictionary in it
    #     one_car = cls(results[0])
    #     return one_car # returns car object
    
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
    #     return one_car # returns property dictionary


    # # Update Property Models

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
    
    