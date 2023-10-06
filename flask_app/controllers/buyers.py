from flask_app import app
from flask import render_template, redirect, request, session, url_for, flash
from flask_app.models import buyer, property, user, address # import entire file, rather than class, to avoid circular imports
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

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
    return redirect("/users/dashboard")

# Read Buyers Controller

@app.route('/buyers/new_buyer_form')
def show_add_buyer_form():
    if "user_id" not in session:
        return redirect("/")
    return render_template("add_buyer.html")

@app.route('/buyers/view/<int:buyer_id>')
def get_one_buyer_with_all_addresses(buyer_id):
        if "user_id" not in session:
            return redirect("/")
        if "logged_in" in session:
            if session['logged_in']:
                one_buyer_with_all_addresses = buyer.Buyer.get_one_buyer_with_all_addresses(buyer_id)
                return render_template("all_properties_for_one_buyer.html", one_buyer_with_all_addresses=one_buyer_with_all_addresses)
        return redirect("/users/logout")

    
@app.route('/buyers/get_all_buyers/<int:realtor_id>')
def get_all_buyers(realtor_id):
    if "user_id" not in session:
        return redirect("/")
    one_user_with_all_buyers = buyer.Buyer.get_all_buyers_for_one_user(realtor_id)

    return render_template("all_buyers_dashboard.html", one_user_with_all_buyers=one_user_with_all_buyers)

# Update Buyers Controller

@app.route('/buyers/edit_buyer_status/<int:buyer_id>', methods=['POST'])
def edit_buyer_status(buyer_id):
    if "user_id" not in session:
        return redirect("/")

    if not session['logged_in']:
        return redirect("/")

    one_buyer = buyer.Buyer.update_buyer_status(request.form)
    if one_buyer:
        flash("Buyer status updated", "success")

    return redirect('/users/dashboard')

# Delete Buyers Controller

@app.route('/buyers/delete/<int:buyer_id>')
def delete_buyer(buyer_id):
    if "user_id" not in session:
        return redirect("/")
    buyer.Buyer.delete_buyer(buyer_id)
    return redirect('/users/dashboard')
