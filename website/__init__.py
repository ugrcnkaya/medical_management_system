from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager #manage user sessions

#database

db = SQLAlchemy()
DB_NAME = "defaultdb"


def create_app():
    # configuration
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '2913AS281ANYSECRETKEY2310'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://doadmin:AVNS_sADnTRke7m5xdFsODkz@db-srh-sdp-do-user-12936967-0.b.db.ondigitalocean.com:25060/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # blueprints - routes
    from .views import  views
    from .auth import  auth
    # prefix for views within the blueprints and register
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    create_database(app)

    ##session settings
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')
