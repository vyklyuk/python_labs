from contextlib import contextmanager
from functools import wraps

from models import Session


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
