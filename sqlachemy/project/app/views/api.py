from flask import Blueprint
from flask import request
from flask import render_template

from app.models import Users
from app import db

user = Blueprint("user", __name__)


@user.route("/login", methods=["POST", "GET"])
def user_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # from sqlalchemy.orm import sessionmaker
        # Session = sessionmaker(engine)
        # db_sesson = Session()
        # 现在不用了,因为 Flask-SQLAlchemy 也已经为我们做好会话打开的工作
        db.session.add(Users(username=username, password=password))
        db.session.commit()

        # 然后再查询,捏哈哈哈哈哈
        user_info = Users.query.filter(
            Users.username == username and Users.password == password).first()
        print(user_info.username)
        if user_info:
            return f"登录成功{user_info.username}"

    return render_template("login.html")
