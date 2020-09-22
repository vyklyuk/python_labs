
from flask import Blueprint

api_blueprint = Blueprint('api', __name__)
STUDENT_ID = 3


@api_blueprint.route(f"/hello-world-{STUDENT_ID}")
def hello_world():
    return f"Hello, World {STUDENT_ID}"