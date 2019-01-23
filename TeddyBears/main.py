from flask import Flask
from flask import render_template

from server.get_content import app_content
from server.get_anything import app_anything
from server.userinfo import users
from server.devices import devices
from server.friends import friends

api = Flask(__name__, template_folder="templates", static_url_path="/static")

api.register_blueprint(app_content)
api.register_blueprint(app_anything)
api.register_blueprint(users)
api.register_blueprint(devices)
api.register_blueprint(friends)


@api.route("/")
def toy():
    return render_template("toy.html")


if __name__ == '__main__':
    api.run("0.0.0.0", 9527, debug=True)
