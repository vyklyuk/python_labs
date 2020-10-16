import os

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    BigInteger,
    DateTime,
    Binary,
    func,
)
from sqlalchemy import orm
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


DB_URI = os.getenv("DB_URI", "postgres://postgres:dagger@localhost:5432/wallets")
engine = create_engine(DB_URI)
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)

BaseModel = declarative_base()


class Users(BaseModel):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(Binary)
    first_name = Column(String)
    last_name = Column(String)


class Wallets(BaseModel):
    __tablename__ = "wallets"

    uid = Column(Integer, primary_key=True)
    name = Column(String)
    funds = Column(BigInteger)
    owner_uid = Column(Integer, ForeignKey(Users.uid))

    owner = orm.relationship(Users, backref="wallets", lazy="joined")


class Transactions(BaseModel):
    __tablename__ = "transactions"

    uid = Column(Integer, primary_key=True)
    from_wallet_uid = Column(Integer, ForeignKey(Wallets.uid))
    to_wallet_uid = Column(Integer, ForeignKey(Wallets.uid))
    amount = Column(BigInteger)
    datetime = Column(DateTime, server_default=func.now())

    from_wallet = orm.relationship(
        Wallets, foreign_keys=[from_wallet_uid], backref="transactions_from", lazy="joined"
    )
    to_wallet = orm.relationship(
        Wallets, foreign_keys=[to_wallet_uid], backref="transactions_to", lazy="joined"
    )
