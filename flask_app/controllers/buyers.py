from flask_app import app
from flask import render_template, redirect, request, session, url_for, flash
from flask_app.models import buyer, property, user, address # import entire file, rather than class, to avoid circular imports
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# As you add model files add them the the import above
# This file is the second stop in Flask's thought process, here it looks for a route that matches the request

# Create Buyers Controller

@app.route('/buyers/create_buyer', methods=["POST"])
def add_buyer():
    if "user_id" not in session:
        return redirect("/")
    if request.form["which_form"] == "create_buyer":
        one_buyer = buyer.Buyer.create_buyer(request.form)
        if not one_buyer:
            flash("Unable to add buyer.", "error")
            return render_template("add_buyer.html")
    return redirect("/buyers/get_all_buyers")

# # Read Buyers Controller


# # @app.route('/dashboard')
# # def show_dashboard():
# #     if "logged_in" in session:
# #         if session['logged_in']:
# #             return render_template("all_cars_dashboard.html", all_cars_with_users=buyer.Car.get_all_cars_and_users())
# #             # return render_template("all_cars_dashboard.html", user=user.User.get_user_by_id(session['user_id']), all_recipes=recipe.Recipe.get_all_recipes_and_users())
# #     return redirect("/users/logout")

@app.route('/buyers/new_buyer_form')
def show_add_buyer_form():
    if "user_id" not in session:
        return redirect("/")
    return render_template("add_buyer.html")

# @app.route('/buyers/get_all')
# def get_all_cars_with_users():
#     all_cars_with_users=buyer.Car.get_all_cars_and_users()
#     return render_template("all_cars_dashboard.html", all_cars_with_users=all_cars_with_users) 
    
@app.route('/buyers/get_all_buyers')
def get_all_buyers():
    all_buyers = buyer.Buyer.get_all_buyers()

    return render_template("all_buyers_dashboard.html", all_buyers=all_buyers)

# @app.route('/show/<int:car_id>')
# def show_one_car(car_id): 
#     if "logged_in" in session:
#         if session['logged_in']:
#             one_car = buyer.Car.get_car_by_id_with_user(car_id)
#             print("^^^^^^^^^^^^^^^^^^^^^")
#             return render_template("view_car.html", one_car=one_car)
#     return redirect("/users/logout")

# # Update Buyers Controller

@app.route('/buyers/edit_buyer_status/<int:buyer_id>', methods=['POST'])
def edit_buyer_status(buyer_id):

    if not session['logged_in']:
        return redirect("/")
    
    # buyer_data = {
    #     "id" : buyer_id,
    #     "status" : request.form["status"]
    # }

    one_buyer = buyer.Buyer.update_buyer_status(request.form)
    if one_buyer:
        flash("Buyer status updated", "success")

    return redirect('/users/dashboard')

# @app.route('/edit/<int:car_id>')
# def show_update_car_form(car_id):
#     if "logged_in" in session:
#         if session['logged_in']:
#             one_car = buyer.Car.get_car_by_id(car_id)
#             return render_template("edit_car.html", one_car=one_car)  
#     return redirect("/users/logout")    

# @app.route('/cars/update/<int:car_id>', methods=['POST'])
# def update_car(car_id):

#     if "user_id" not in session:
#         return redirect("/")
    
#     if request.form["which_form"] == "edit_car":
#         one_car = buyer.Car.update_car(request.form)

#         if not one_car:
#             path = f"/edit/{car_id}"    
#             return redirect(path)
#     return redirect('/dashboard')

# # Delete Buyers Controller

# @app.route('/cars/delete/<int:id>')
# def delete_car(id):
#     if "user_id" not in session:
#         return redirect("/")
#     buyer.Car.delete_car(id)
#     return redirect('/cars/get_all')

# @app.route('/cars/purchase/<int:id>')
# def purchase_car(id):
#     if "user_id" not in session:
#         return redirect("/")
#     buyer.Car.purchase_car(id)
#     return redirect('/cars/get_all')