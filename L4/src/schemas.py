from marshmallow import validate, Schema, fields


class Credentials(Schema):
    email = fields.String(validate=validate.Email())
    password = fields.String()


class AccessToken(Schema):
    access_token = fields.String()


class ListUsersRequest(Schema):
    email = fields.String(validate=validate.Email())
    first_name = fields.String()
    last_name = fields.String()


class UserData(Schema):
    uid = fields.Integer()
    email = fields.String(validate=validate.Email())
    first_name = fields.String()
    last_name = fields.String()


class UserToCreate(Schema):
    email = fields.String(validate=validate.Email())
    password = fields.String()
    first_name = fields.String()
    last_name = fields.String()


class UserToUpdate(Schema):
    email = fields.String(validate=validate.Email())
    password = fields.String()
    first_name = fields.String()
    last_name = fields.String()


class WalletData(Schema):
    uid = fields.Integer()
    name = fields.String()
    funds = fields.Integer()


class WalletToCreate(Schema):
    name = fields.String()


class WalletToUpdate(Schema):
    name = fields.String()


class FundsToSend(Schema):
    to_wallet = fields.Integer()
    amount = fields.Integer()


class TransactionData(Schema):
    uid = fields.Integer()
    from_wallet = fields.Integer(attribute="from_wallet_uid")
    to_wallet = fields.Integer(attribute="to_wallet_uid")
    amount = fields.Integer()
    datetime = fields.DateTime()


class StatusResponse(Schema):
    code = fields.Integer()
    type = fields.String(default="OK")
    message = fields.String(default="OK")
