from flask_app import app
from flask import render_template, redirect, request, session, url_for, flash
from flask_app.models import buyer, property, user, address # import entire file, rather than class, to avoid circular imports
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# As you add model files add them the the import above
# This file is the second stop in Flask's thought process, here it looks for a route that matches the request

# Create Properties Controller

@app.route('/properties/create_property/<int:buyer_id>/<int:address_id>', methods=["POST"])
def add_property(buyer_id, address_id):
    if "user_id" not in session:
        return redirect("/")
    if request.form["which_form"] == "create_property":
        property_id = property.Property.create_property(request.form)
        if not property_id:
            flash("Unable to add property.", "error")
            buyer_info = buyer.Buyer.get_buyer_by_id(buyer_id)
            address_info = address.Address.get_address_by_id(address_id)
            return render_template("add_property_info_form.html", buyer_info=buyer_info, address_info=address_info)
    route_path = f"/addresses/view/{buyer_id}"    
    return redirect(route_path)

# # Read Properties Controller


# @app.route('/dashboard')
# def show_dashboard():
#     if "logged_in" in session:
#         if session['logged_in']:
#             return render_template("all_cars_dashboard.html", all_cars_with_users=buyer.Car.get_all_cars_and_users())
#             # return render_template("all_cars_dashboard.html", user=user.User.get_user_by_id(session['user_id']), all_recipes=recipe.Recipe.get_all_recipes_and_users())
#     return redirect("/users/logout")

# @app.route('/new')
# def show_create_car_form():
#     if "user_id" not in session:
#         return redirect("/")
#     return render_template("sell_car.html", price="0", year="0")

# @app.route('/cars/get_all')
# def get_all_cars_with_users():
#     all_cars_with_users=buyer.Car.get_all_cars_and_users()
#     return render_template("all_cars_dashboard.html", all_cars_with_users=all_cars_with_users) 

@app.route('/properties/new_property_info_form/<int:buyer_id>/<int:address_id>')
def show_add_property_info_form(buyer_id, address_id):
    if "user_id" not in session:
        return redirect("/")
    buyer_info = buyer.Buyer.get_buyer_by_id(buyer_id)
    address_info = address.Address.get_address_by_id(address_id)
    return render_template("add_property_info_form.html", buyer_info=buyer_info, address_info=address_info)

    
# @app.route('/show/<int:car_id>')
# def show_one_car(car_id): 
#     if "logged_in" in session:
#         if session['logged_in']:
#             one_car = buyer.Car.get_car_by_id_with_user(car_id)
#             print("^^^^^^^^^^^^^^^^^^^^^")
#             return render_template("view_car.html", one_car=one_car)
#     return redirect("/users/logout")

# # Update Properties Controller

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

# # Delete Properties Controller

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