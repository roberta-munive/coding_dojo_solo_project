from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user
import re, datetime
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


class Buyer:
    db = "noteworthy_properties_schema" 
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.status = data['status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.realtor = None
        
    # Create Buyer Models

    # class method to save our buyer to the database
    @classmethod
    def create_buyer(cls, buyer_data):

        if not cls.validate_buyer(buyer_data):
            return False
        
        buyer_data = buyer_data.copy()

        query = """
                INSERT INTO buyers (first_name, last_name, status, user_id) 
                VALUES (%(first_name)s, %(last_name)s, %(status)s, %(user_id)s);
        """

        buyer_id = connectToMySQL(cls.db).query_db(query, buyer_data)

        return buyer_id

    # Read Buyer Models

    @classmethod
    def get_all_buyers(cls):
        query = """
                SELECT * FROM buyers;
                """
        results = connectToMySQL(cls.db).query_db(query)
        all_buyers = []
        for result in results:
            this_buyer = cls(result)
            all_buyers.append(this_buyer)
        return all_buyers
    
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


    # # the get_buyer_by_id method will be used when we need to retrieve just one specific row of the table
    @classmethod
    def get_buyer_by_id(cls, id):
        query = """
                SELECT * FROM buyers
                WHERE id = %(id)s;
        """
        data = {'id': id}
        results = connectToMySQL(cls.db).query_db(query, data)  # a list with one dictionary in it
        one_buyer = cls(results[0])
        return one_buyer # returns buyer object
    
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
    #     return one_car # returns buyer dictionary


    # # Update Buyer Models

    @classmethod
    def update_buyer_status(cls, buyer_data):

            this_buyer = cls.get_buyer_by_id(buyer_data['id'])
            if session['user_id'] != this_buyer.user_id:
                return False
        
            query = """
                    UPDATE buyers
                    SET status = %(status)s
                    WHERE id=%(id)s;    
            """
            connectToMySQL(cls.db).query_db(query, buyer_data)
            return True

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
    

    # # Delete Buyer Models

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
    def validate_buyer(buyer):
        is_valid = True
        if len(buyer['first_name']) < 1 or buyer['first_name'].isspace():
            flash("First name is required.", "error")
            is_valid = False
        if len(buyer['last_name']) < 1 or buyer['last_name'].isspace():
            flash("Last name is required.", "error")
            is_valid = False                         
        return is_valid
    
    