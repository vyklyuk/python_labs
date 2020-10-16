from datetime import timedelta

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt import JWT
from sqlalchemy.orm.exc import NoResultFound

from lab5.auth import authenticate, identity
from lab5.blueprint import api_blueprint
from lab5.error_handlers import not_found, server_error, not_authorized

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_AUTH_URL_RULE'] = '/api/v1/auth'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=1)
app.config['JWT_AUTH_URL_OPTIONS'] = {'methods': ['POST'], 'endpoint': 'auth'}

app.register_blueprint(api_blueprint, url_prefix="/api/v1")

app.register_error_handler(NoResultFound, not_found)
app.register_error_handler(Exception, server_error)

jwt = JWT(app, authenticate, identity)
jwt.jwt_error_handler(not_authorized)

bcrypt = Bcrypt(app)
