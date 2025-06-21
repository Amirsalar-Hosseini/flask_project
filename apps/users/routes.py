import flask
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user

from apps.users.forms import RegisterForm, LoginForm
from apps.users.models import User
from apps.extensions import hashing, db

blueprint = Blueprint('users', __name__)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print('helooooooooooooooooooooooooooooooooooo')
        hashed_password = hashing.hash_value(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('user registered successfully', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html', form=form)
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
        if user and hashing.check_value(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flask.flash('login successful', 'success')
            return redirect(url_for('home.home'))
    return render_template('users/login.html', form=form)