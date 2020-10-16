import hashlib
from abc import ABC, abstractmethod

from flask_bcrypt import check_password_hash

from lab5.models import Session, Users


class BaseUserIdentity(ABC):
    @property
    @abstractmethod
    def id(self):
        pass

    @property
    @abstractmethod
    def is_admin(self):
        return False


class UserModelIdentity(BaseUserIdentity):
    def __init__(self, model):
        self.model = model

    @property
    def id(self):
        return self.model.uid

    @property
    def is_admin(self):
        return False


class AdminUserIdentity(BaseUserIdentity):
    @property
    def id(self):
        from lab5.app import app
        return hashlib.sha256(app.config['SECRET_KEY'].encode()).hexdigest()

    @property
    def is_admin(self):
        return True


def authenticate(username, password):
    from lab5.app import app
    session = Session()
    admin_identity = AdminUserIdentity()
    if username == f'admin-{admin_identity.id}' and password == app.config['SECRET_KEY']:
        return admin_identity
    else:
        user = session.query(Users).filter_by(email=username).one()
        if user and check_password_hash(user.password, password):
            return UserModelIdentity(user)


def identity(payload):
    admin_identity = AdminUserIdentity()
    if payload['identity'] == admin_identity.id:
        return admin_identity
    else:
        session = Session()
        return UserModelIdentity(
            session.query(Users).filter_by(uid=payload['identity']).one()
        )
