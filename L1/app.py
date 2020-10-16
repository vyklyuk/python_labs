from flask import Flask

from .blueprint import api_blueprint

app = Flask(__name__)
app.register_blueprint(api_blueprint, url_prefix="/api/v1")

if __name__ == '__main__':
    app.run()