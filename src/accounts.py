from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .decorators import check_logged


#blue print to create the endpoints
accounts = Blueprint('accounts', __name__)


@accounts.route('/login', methods=['GET', 'POST'])
@check_logged
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password1')

        user = User.query.filter_by(email=email).first()
        if user:
            #checking if the 2 hashes match
            if check_password_hash(user.password, password):
                flash('Log in successful', category='success')
                login_user(user, remember=True) 
                return redirect(url_for('views.index'))
            else:
                flash('Password incorrect', category='error')
        else:
            flash('That user doesnt exist', category='error')
        
    return render_template('login.html')


@accounts.route('/register', methods=['GET', 'POST'])
@check_logged
def register():
    if request.method == 'POST':
        #getting form data
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        check_user = User.query.filter_by(email=email).first()
        if check_user:
            flash('that email already exists, use  another one', category='error')
        elif len(email) < 15:
            flash('email too short try again!', category='error')
        elif len(first_name) < 2:
            flash('first name is too short', category='error')
        elif len(last_name) < 2:
            flash('last name is too short', category='error')
        elif password1 != password2:
            flash('passwords dont match try again', category='error')
        else:
            #creating new user if everything is ok
            new_user = User(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('User created successfuly!', category='success')
            return redirect(url_for('accounts.login'))

    return render_template('register.html')


@accounts.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('accounts.login'))
