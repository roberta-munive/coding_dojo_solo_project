from flask_app import app
from flask import render_template, redirect, request, session, url_for, flash
from flask_app.models import buyer, property, user, address # import entire file, rather than class, to avoid circular imports
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Create Properties Controller

@app.route('/properties/create_property/<int:buyer_id>/<int:address_id>', methods=["POST"])
def add_property(buyer_id, address_id):
    if "user_id" not in session:
        return redirect("/")
    if request.form["which_form"] == "create_property":
        property_id = property.Property.create_property(request.form)
        if not property_id:
            flash("Unable to add property.", "error")
            one_address_with_buyer_info = address.Address.get_one_address_with_buyer_info(address_id)
            return render_template("add_property_info_form.html", one_address_with_buyer_info=one_address_with_buyer_info)
    route_path = f"/buyers/view/{buyer_id}"    
    return redirect(route_path)

# Read Properties Controller

@app.route('/properties/new_property_info_form/<int:address_id>')
def show_add_property_info_form(address_id):
    if "user_id" not in session:
        return redirect("/")
    one_address_with_buyer_info = address.Address.get_one_address_with_buyer_info(address_id)
    return render_template("add_property_info_form.html", one_address_with_buyer_info=one_address_with_buyer_info)

# Update Properties Controller

@app.route('/properties/edit_property_form/<int:address_id>')
def show_update_property_form(address_id):
    if "user_id" not in session:
        return redirect("/")
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

# Delete Properties Controller