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
            # buyer_info = buyer.Buyer.get_buyer_by_id(buyer_id) *******************
            # address_info = address.Address.get_address_by_id(address_id)***************
            one_address_with_buyer_info = address.Address.get_one_address_with_buyer_info(address_id)
            return render_template("add_property_info_form.html", one_address_with_buyer_info=one_address_with_buyer_info)
    route_path = f"/buyers/view/{buyer_id}"    
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

@app.route('/properties/new_property_info_form/<int:address_id>')
def show_add_property_info_form(address_id):
    if "user_id" not in session:
        return redirect("/")
    one_address_with_buyer_info = address.Address.get_one_address_with_buyer_info(address_id)
    return render_template("add_property_info_form.html", one_address_with_buyer_info=one_address_with_buyer_info)

    
# @app.route('/show/<int:car_id>')
# def show_one_car(car_id): 
#     if "logged_in" in session:
#         if session['logged_in']:
#             one_car = buyer.Car.get_car_by_id_with_user(car_id)
#             print("^^^^^^^^^^^^^^^^^^^^^")
#             return render_template("view_car.html", one_car=one_car)
#     return redirect("/users/logout")

# # Update Properties Controller

@app.route('/properties/edit_property_form/<int:address_id>')
def show_update_property_form(address_id):
    if "logged_in" in session:
        if session['logged_in']:
            one_address_with_property_and_buyer_info = address.Address.get_one_address_with_property_and_buyer_info(address_id)
            return render_template("edit_property_info_form.html", one_address_with_property_and_buyer_info=one_address_with_property_and_buyer_info)  
    return redirect("/users/logout")    

@app.route('/properties/update_property/<int:address_id>/<int:property_id>', methods=['POST'])
def update_property(address_id, property_id):

    if "user_id" not in session:
        return redirect("/")
    
    if request.form["which_form"] == "edit_property":

        one_property = property.Property.update_property(request.form)

        if not one_property:
            flash("Unable to update property.", "error")
            path = f"/properties/edit_property_form/{address_id}"    
            return redirect(path)
    one_address_with_property_and_buyer_info = address.Address.get_one_address_with_property_and_buyer_info(address_id)
    path = f"/addresses/view_one/{address_id}"
    return redirect(path)

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