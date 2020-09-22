from flask import Flask

app = Flask(__name__)
STUDENT_ID = 3


@app.route(f"/hello-world-{STUDENT_ID}")
def hello_world():
    return f"Hello, World {STUDENT_ID}"

if __name__ == '__main__':
    app.run()