from flask import Blueprint, render_template, redirect, url_for
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
        return redirect(url_for('users.login'))
    return render_template('users/register.html', form=form)
@blueprint.route('/login')
def login():
    form = LoginForm()
    return render_template('users/login.html', form=form)