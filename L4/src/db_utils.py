from sqlalchemy import or_

from models import Session, Users, Wallets, Transactions


def list_users(email=None, first_name=None, last_name=None):
    session = Session()
    filters = []
    if email:
        filters.append(Users.email.like(email))
    if first_name:
        filters.append(Users.email.like(first_name))
    if last_name:
        filters.append(Users.email.like(last_name))
    return session.query(Users).filter(*filters).all()


def list_wallets():
    session = Session()
    return session.query(Wallets).all()


def list_transactions_for_wallet(wallet_id):
    session = Session()
    return (
        session.query(Transactions)
        .filter(
            or_(
                Transactions.from_wallet_uid == wallet_id,
                Transactions.to_wallet_uid == wallet_id,
            )
        )
        .all()
    )


def create_entry(model_class, *, commit=True, **kwargs):
    session = Session()
    entry = model_class(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
    return entry


def get_entry_by_uid(model_class, uid):
    session = Session()
    return session.query(model_class).filter_by(uid=uid).one()


def update_entry(entry, *, commit=True, **kwargs):
    session = Session()
    for key, value in kwargs.items():
        setattr(entry, key, value)
    if commit:
        session.commit()
    return entry


def delete_entry(model_class, uid, *, commit=True):
    session = Session()
    session.query(model_class).filter_by(uid=uid).delete()
    if commit:
        session.commit()
