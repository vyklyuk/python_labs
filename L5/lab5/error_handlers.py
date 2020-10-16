import logging
from traceback import format_exc

from flask import jsonify

from lab5.schemas import StatusResponse


def not_authorized(e):
    return error_handler(e, code=401, type='NOT_AUTHORIZED', message_prefix='Not authorized')


def not_found(e):
    return error_handler(e, code=404, type='NOT_FOUND', message_prefix='Not found')


def server_error(e):
    return error_handler(e, code=500, type='SERVER_ERROR', message_prefix='Server error')


def error_handler(e, code, type, message_prefix):
    logging.exception(format_exc())
    return jsonify(
        StatusResponse().dump(
            {
                "code": code,
                "type": type,
                "message": f"{message_prefix}: {e!r}"
            }
        )
    ), code
