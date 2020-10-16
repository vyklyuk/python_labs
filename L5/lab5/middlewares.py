from contextlib import contextmanager
from functools import wraps

from flask import jsonify
from flask_jwt import current_identity

from lab5.models import Session
from lab5.schemas import StatusResponse


def db_lifecycle(func):
    @wraps(func)
    def inner(*args, **kwargs):
        with db_session_context():
            return func(*args, **kwargs)
    return inner


@contextmanager
def db_session_context():
    session = Session()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    else:
        try:
            session.commit()
        except Exception:
            session.rollback()
            raise


def only_admin_access(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not current_identity.is_admin:
            return jsonify(StatusResponse().dump({
                "code": 401,
                "type": "NOT_AUTHORIZED",
                "message": "Only Admin is allowed to access this endpoint",
            })), 401
        return func(*args, **kwargs)
    return inner


def only_target_authorized_user_access_or_admin(func):
    @wraps(func)
    def inner(user_id, *args, **kwargs):
        if current_identity.id != user_id and not current_identity.is_admin:
            return jsonify(StatusResponse().dump({
                "code": 401,
                "type": "NOT_AUTHORIZED",
                "message": f"You're trying to access endpoint only available for user {user_id}",
            })), 401
        return func(user_id, *args, **kwargs)
    return inner
