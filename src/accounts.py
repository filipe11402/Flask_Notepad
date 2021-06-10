from flask import Blueprint


accounts = Blueprint('accounts', __name__)


@accounts.route('/login')
def login():
    return '<p>Login</p>'


@accounts.route('/register')
def register():
    return '<p>Register</p>'


@accounts.route('/logout')
def logout():
    return '<p>Logout</p>'
