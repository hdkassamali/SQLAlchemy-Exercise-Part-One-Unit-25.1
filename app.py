"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "blogproject12345"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

# When working in ipython or when using unittest framework run the line below:
# app.app_context().push()

connect_db(app)


@app.route("/")
def root():
    """Homepage redirects to list of users."""

    return redirect("/users")


@app.route("/users")
def homepage():
    """Show a page with info on all users"""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/users/new")
def new_user_form():
    """Show a form to create a new user"""

    return render_template("new_user_form.html")


@app.route("/users/new", methods=["POST"])
def add_new_user():
    """Handle form submission for creating a new user"""

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def user_details(user_id):
    """Show a page with info on a specific user"""

    user = User.query.get_or_404(user_id)
    return render_template("user_details.html", user=user)


@app.route("/users/<int:user_id>/edit")
def user_edit_page(user_id):
    """Show a form to edit an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template("user_edit_page.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user_details(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Handle form submission for deleting an existing user"""

    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect("/users")