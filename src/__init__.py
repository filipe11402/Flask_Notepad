from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = 'base_dados.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'filipe'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .accounts import accounts

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'accounts.login'

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(accounts, url_prefix='/accounts')

    return app


def create_database(app):
    if not path.exists('src/' + DB_NAME):
        db.create_all(app=app)
        print("DATABASE CREATED")
