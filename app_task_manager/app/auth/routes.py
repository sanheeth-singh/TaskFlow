from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db
from ..models import User
from ..forms import RegisterForm, LoginForm

# Define the Blueprint
auth = Blueprint('auth', __name__)


@auth.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("This email is already registered, Please Login", category="error")
            return redirect(url_for("auth.register", form=form))  # Note: auth.register

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data, method='pbkdf2:sha256')
        )

        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        flash("Account created successfully!", category="success")
        return redirect(url_for("main.home"))  # Redirect to main blueprint
    return render_template("auth/register.html", form=form)


@auth.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            return redirect(url_for("main.home"))
        flash("Invalid credentials", category="error")
    return render_template("auth/login.html", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    flash("You have logged-out")
    return redirect(url_for("auth.login"))
