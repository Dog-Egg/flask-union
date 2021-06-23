from flask import Flask
from flask_union import FlaskUnion

app = Flask(__name__)

union = FlaskUnion(app)


def view1():
    return 1


def view2():
    return 2


@union.route('/', [view1, view2])
def index(result):
    return result


if __name__ == '__main__':
    app.run()
