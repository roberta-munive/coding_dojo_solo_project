from flask_app import app
from flask import render_template, redirect, request, session, url_for, flash
from flask_app.models import buyer, property, user, address # import entire file, rather than class, to avoid circular imports
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Create Addresses Controller

@app.route('/addresses/create_address/<int:buyer_id>', methods=["POST"])
def add_address(buyer_id):
    if "user_id" not in session:
        return redirect("/")
    if request.form["which_form"] == "create_address":
        address_id =  address.Address.create_address(request.form)
        if not address_id:
            buyer_info = buyer.Buyer.get_buyer_by_id(buyer_id)
            flash("Unable to add address.", "error")
            return render_template("add_property_address_form.html", buyer_info=buyer_info)
    route_path = f"/properties/new_property_info_form/{address_id}"  
    return redirect(route_path)

# Read Addresses Controller

@app.route('/addresses/new_property_address_form/<int:buyer_id>')
def show_add_property_address_form(buyer_id):
    if "user_id" not in session:
        return redirect("/")
    buyer_info = buyer.Buyer.get_buyer_by_id(buyer_id)
    return render_template("add_property_address_form.html", buyer_info=buyer_info)

@app.route('/addresses/view_one/<int:address_id>')
def get_one_address_with_property_and_buyer_info(address_id):
        if "user_id" not in session:
            return redirect("/")
        if "logged_in" in session:
            if session['logged_in']:
                one_address_with_property_and_buyer_info = address.Address.get_one_address_with_property_and_buyer_info(address_id)
                return render_template("view_property.html", one_address_with_property_and_buyer_info=one_address_with_property_and_buyer_info)
        return redirect("/users/logout")

# Delete Addresses Controller

@app.route('/addresses/delete/<int:address_id>/<int:buyer_id>')
def delete_address(address_id, buyer_id):
    if "user_id" not in session:
        return redirect("/")
    address.Address.delete_address(address_id)
    route_path = f"/buyers/view/{buyer_id}"
    return redirect(route_path)
