from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

#database

db = SQLAlchemy()
DB_NAME = "defaultdb"


def create_app():
    # configuration
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SECRETKEY'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://doadmin:AVNS_sADnTRke7m5xdFsODkz@db-srh-sdp-do-user-12936967-0.b.db.ondigitalocean.com:25060/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # blueprints

    from .views import  views
    from .auth import  auth
    # prefix for views within the blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    create_database(app)

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')
