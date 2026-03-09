from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()


def create_app():
    # Get the absolute path to the static folder
    static_folder = os.path.join(os.path.dirname(__file__), '..', 'static')
    app = Flask(__name__, template_folder='templates', static_folder=static_folder)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appdata.db'
    app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
    db.init_app(app)

    # TODO: create and register all blueprints
    from requests_application.core.routes import core
    from requests_application.users.routes import users
    from requests_application.cit_request.routes import cit_request

    app.register_blueprint(core, url_prefix='/')
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(cit_request, url_prefix='/cit_request')

    migrate = Migrate(app,db)


    return app

