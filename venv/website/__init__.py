from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()
DB_NAME = 'datamapFiles.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    #app.register_blueprint(auth, url_prefix='/')
    # from . import models
    # create_database(app)
    return app

# def create_database(app):
#     if not db.exists(DB_NAME):
#         db.create_all(app=app)
#         print('Created Database!')
#     else:
#         print('Database already exists!')