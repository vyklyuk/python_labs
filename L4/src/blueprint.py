from flask import Blueprint, jsonify, request

import db_utils
from middlewares import db_lifecycle
from models import Users, Wallets, Transactions
from schemas import (
    Credentials,
    AccessToken,
    UserData,
    ListUsersRequest,
    UserToCreate,
    UserToUpdate,
    StatusResponse,
    WalletData,
    WalletToCreate,
    WalletToUpdate, TransactionData, FundsToSend,
)

api_blueprint = Blueprint('api', __name__)


@api_blueprint.route("/auth", methods=["POST"])
def auth():
    Credentials().load(request.json)
    return jsonify(AccessToken().dump({"access_token": ""}))


@api_blueprint.route("/user", methods=["GET"])
@db_lifecycle
def list_users():
    args = ListUsersRequest().load(request.args)
    users = db_utils.list_users(
        args.get("email"), args.get("first_name"), args.get("last_name")
    )
    return jsonify(UserData(many=True).dump(users))


@api_blueprint.route("/user", methods=["POST"])
@db_lifecycle
def create_user():
    user_data = UserToCreate().load(request.json)
    user = db_utils.create_entry(Users, **user_data)
    return jsonify(UserData().dump(user))


@api_blueprint.route("/user/<int:user_id>", methods=["GET"])
@db_lifecycle
def get_user_by_id(user_id):
    user = db_utils.get_entry_by_uid(Users, user_id)
    return jsonify(UserData().dump(user))


@api_blueprint.route("/user/<int:user_id>", methods=["PUT"])
@db_lifecycle
def update_user(user_id):
    user_data = UserToUpdate().load(request.json)
    user = db_utils.get_entry_by_uid(Users, user_id)
    db_utils.update_entry(user, **user_data)
    return jsonify(StatusResponse().dump({"code": 200}))


@api_blueprint.route("/user/<int:user_id>", methods=["DELETE"])
@db_lifecycle
def delete_user(user_id):
    db_utils.delete_entry(Users, user_id)
    return jsonify(StatusResponse().dump({"code": 200}))


@api_blueprint.route("/wallet", methods=["GET"])
@db_lifecycle
def list_wallets():
    wallets = db_utils.list_wallets()
    return jsonify(WalletData(many=True).dump(wallets))


@api_blueprint.route("/wallet", methods=["POST"])
@db_lifecycle
def create_wallet():
    wallet_data = WalletToCreate().load(request.json)
    wallet = db_utils.create_entry(Wallets, **wallet_data, funds=0)
    return jsonify(WalletData().dump(wallet))


@api_blueprint.route("/wallet/<int:wallet_id>", methods=["GET"])
@db_lifecycle
def get_wallet_by_id(wallet_id):
    wallet = db_utils.get_entry_by_uid(Wallets, wallet_id)
    return jsonify(WalletData().dump(wallet))


@api_blueprint.route("/wallet/<int:wallet_id>", methods=["PUT"])
@db_lifecycle
def update_wallet(wallet_id):
    wallet_data = WalletToUpdate().load(request.json)
    wallet = db_utils.get_entry_by_uid(Wallets, wallet_id)
    db_utils.update_entry(wallet, **wallet_data)
    return jsonify(StatusResponse().dump({"code": 200}))


@api_blueprint.route("/wallet/<int:wallet_id>", methods=["DELETE"])
@db_lifecycle
def delete_wallet(wallet_id):
    db_utils.delete_entry(Wallets, wallet_id)
    return jsonify(StatusResponse().dump({"code": 200}))


@api_blueprint.route("/wallet/<int:wallet_id>/send-funds", methods=["POST"])
@db_lifecycle
def send_funds(wallet_id):
    transaction_data = FundsToSend().load(request.json)

    from_wallet = db_utils.get_entry_by_uid(Wallets, wallet_id)
    assert from_wallet.funds > transaction_data["amount"], "Not enough funds"
    db_utils.update_entry(
        from_wallet,
        funds=Wallets.funds - transaction_data["amount"],
        commit=False,
    )

    to_wallet = db_utils.get_entry_by_uid(Wallets, transaction_data["to_wallet"])
    db_utils.update_entry(
        to_wallet,
        funds=Wallets.funds + transaction_data["amount"],
        commit=False,
    )

    transaction = db_utils.create_entry(
        Transactions,
        from_wallet_uid=wallet_id,
        to_wallet_uid=transaction_data["to_wallet"],
        amount=transaction_data["amount"],
    )
    return jsonify(TransactionData().dump(transaction))


@api_blueprint.route("/wallet/<int:wallet_id>/transactions", methods=["GET"])
@db_lifecycle
def list_wallet_transactions(wallet_id):
    transactions = db_utils.list_transactions_for_wallet(wallet_id)
    return jsonify(TransactionData(many=True).dump(transactions))
