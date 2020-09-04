"""Blogly application."""

from flask import Flask, render_template, request, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secretcode123123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/")
def list_users():
    """Shows list of all users in the db"""

    return redirect('/users')

@app.route("/users")
def linked_users():
    """Show a list of users with links to their details, and a button to add a new user"""
    users = User.query.all()
    return render_template ('users.html', users=users)

@app.route("/users/new", methods=["GET"])
def add_user_form():
    """Form to add a new user"""
    return render_template ('add_user.html')

@app.route("/users/new", methods=["POST"])
def add_user():
    """Adds user to db"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    image_url = image_url if image_url else None

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect ('/users')

@app.route('/users/<int:userid>')
def details_page(userid):
    """Shows specified user's details page"""
    user = User.query.get_or_404(userid)
    return render_template("details.html", user=user)

@app.route('/users/<int:userid>/edit')
def edit_user(userid):
    """Edit a specific user"""
    user = User.query.get_or_404(userid)
    return render_template("edit_user.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_db_user(user_id):
    """Update a user based on edits"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    
    return redirect("/users")

@app.route('/users/<int:userid>/delete', methods=["POST"])
def delete_user(userid):
    """Delete a specific user"""
    user = User.query.get(userid)
    db.session.delete(user)
    db.session.commit()
    return redirect ("/users")
