import flask
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from apps.users.forms import RegisterForm, LoginForm, UpdateProfileForm
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
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
            if user and hashing.check_value(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flask.flash('login successful', 'success')
                next_page = request.args.get('next')
                return redirect(next_page if next_page else url_for('home.home'))
            else:
                flask.flash('Email or password is wrong', 'danger')
        return render_template('users/login.html', form=form)

@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flask.flash('logout successful', 'success')
    return redirect(url_for('users.login'))

@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.new_password.data:
            current_user.password = hashing.hash_value(form.new_password.data)
        db.session.commit()
        flask.flash('profile updated successfully', 'success')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('users/profile.html', form=form)