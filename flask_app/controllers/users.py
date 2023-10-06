from flask_app import app
from flask import render_template, redirect, request, session, url_for, flash
from flask_app.models import buyer, property, user, address # import entire file, rather than class, to avoid circular imports
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Create Users Controller

@app.route('/users/register', methods=["POST"])
def create_user():
    if request.form["which_form"] == "register":
        if not user.User.register_user(request.form):
            flash("Unable to add user.", "error")
            return render_template("login_and_registration.html", first_name=request.form["first_name"], last_name=request.form["last_name"], registration_email=request.form["email"] )

    return redirect("/users/dashboard") 

# Read Users Controller

@app.route('/')
def index():
    return render_template("login_and_registration.html")

@app.route('/users/dashboard')
def show_dashboard():
    if "user_id" not in session:
        return redirect("/")
    if "logged_in" in session:
        if session['logged_in']:
            one_user_with_all_buyers = user.User.get_one_user_by_id_with_all_buyers(session['user_id'])
            return render_template("all_buyers_dashboard.html", one_user_with_all_buyers=one_user_with_all_buyers)
    return redirect("/users/logout")

# Update Users Controller


# Delete Users Controller


# Login and Logout

@app.route('/users/logout')
def logout():
    #session.pop("user_id")
    session.clear()  
    return redirect("/")

@app.route('/users/login', methods=['POST'])
def login():

    if not user.User.login_user(request.form):
        return render_template("login_and_registration.html", login_email=request.form["email"])
    return redirect('/users/dashboard')
    
