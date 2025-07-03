from flask import Flask,redirect
import os, sys 

def resource_path(relative_path):
    try:
        base = sys._MEIPASS
    except AttributeError:
        base = os.path.abspath(".")
    return os.path.join(base, relative_path)

def create_app():
    app = Flask(
        __name__,
        static_folder=resource_path("website/static"),
        template_folder=resource_path("website/templates")
    )
    app.config['SECRET_KEY'] = 'your_secret_key'

    from .home import home
    from .auth import auth
    @app.route('/')
    def index():
        return redirect('/login')

    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app