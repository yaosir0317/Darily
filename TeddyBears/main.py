from flask import Flask

from server.get_content import app_content
from server.get_anything import app_anything

api = Flask(__name__)

api.register_blueprint(app_content)
api.register_blueprint(app_anything)


if __name__ == '__main__':
    api.run("0.0.0.0", 9527, debug=True)