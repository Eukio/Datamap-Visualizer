from flask import Flask, redirect



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'

    from .home import home
    from .auth import auth
    @app.route('/')
    def index():
        return redirect('/login')

    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app