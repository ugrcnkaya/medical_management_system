from flask import Flask

app = Flask(__name__)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SECRETKEY'

    ##blueprints

    from .views import  views
    from .auth import  auth
    ##prefix for views within the blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    return app
