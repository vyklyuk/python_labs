from models import Session, Users, Wallets, Transactions

session = Session()

user = Users(uid=1, email="example@example.com", first_name="First", last_name="Last")
wallet_1 = Wallets(uid=1, name="My wallet", funds=90, owner=user)
wallet_2 = Wallets(uid=2, name="My wallet", funds=110, owner=user)
transaction = Transactions(uid=1, from_wallet=wallet_1, to_wallet=wallet_2, amount=10)

session.add(user)
session.add(wallet_1)
session.add(wallet_2)
session.add(transaction)
session.commit()

print(session.query(Users).all())
print(session.query(Wallets).all())
print(session.query(Transactions).all())

session.close()
