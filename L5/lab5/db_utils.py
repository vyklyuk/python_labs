from lab5.models import Session, Users, Wallets, Transactions


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


def list_wallets(*filters):
    session = Session()
    return (
        session.query(Wallets)
        .join(Users)
        .filter(*filters)
        .all()
    )


def list_transactions_for_wallet(user_uid, wallet_id):
    session = Session()
    session.query(Wallets).filter_by(uid=wallet_id, owner_uid=user_uid).one()
    transactions_from = (
        session.query(Transactions)
        .join(Wallets, Transactions.from_wallet_uid == Wallets.uid)
        .filter(
            Wallets.owner_uid == user_uid, Transactions.from_wallet_uid == wallet_id
        )
    )
    transactions_to = (
        session.query(Transactions)
        .join(Wallets, Transactions.to_wallet_uid == Wallets.uid)
        .filter(
            Wallets.owner_uid == user_uid, Transactions.to_wallet_uid == wallet_id
        )
    )
    return (
        transactions_from.union(transactions_to)
        .order_by(Transactions.datetime)
        .all()
    )


def create_entry(model_class, *, commit=True, **kwargs):
    session = Session()
    entry = model_class(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
    return entry


def get_entry_by_uid(model_class, uid, **kwargs):
    session = Session()
    return session.query(model_class).filter_by(uid=uid, **kwargs).one()


def update_entry(entry, *, commit=True, **kwargs):
    session = Session()
    for key, value in kwargs.items():
        setattr(entry, key, value)
    if commit:
        session.commit()
    return entry


def delete_entry(model_class, uid, *, commit=True, **kwargs):
    session = Session()
    session.query(model_class).filter_by(uid=uid, **kwargs).delete()
    if commit:
        session.commit()
