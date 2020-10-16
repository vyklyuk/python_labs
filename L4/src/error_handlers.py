import logging
from traceback import format_exc

from flask import jsonify

from schemas import StatusResponse


def not_found(e):
    logging.exception(format_exc())
    return jsonify(
        StatusResponse().dump(
            {
                "code": 404,
                "type": "NOT_FOUND",
                "message": f"Not found: {e!r}"
            }
        )
    ), 404


def server_error(e):
    logging.exception(format_exc())
    return jsonify(
        StatusResponse().dump(
            {
                "code": 500,
                "type": "SERVER_ERROR",
                "message": f"Not found: {e!r}"
            }
        )
    ), 500
