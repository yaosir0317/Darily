from flask import Flask
# 导入Flask-SQLAlchemy中的SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

from .views.api import user
# 实例化SQLAlchemy;实例化SQLAlchemy的代码必须要在引入蓝图之前
db = SQLAlchemy()

# 引入蓝图


def create_app():
    app = Flask(__name__)

    # 初始化App配置 这个app配置专门针对 SQLAlchemy 进行配置
    # SQLALCHEMY_DATABASE_URI 配置 SQLAlchemy 的链接字符串儿
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@127.0.0.1:3306/db2019?charset=utf8"
    # SQLALCHEMY_POOL_SIZE 配置 SQLAlchemy 的连接池大小
    app.config["SQLALCHEMY_POOL_SIZE"] = 5
    # SQLALCHEMY_POOL_TIMEOUT 配置 SQLAlchemy 的连接超时时间
    app.config["SQLALCHEMY_POOL_TIMEOUT"] = 15
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # 初始化SQLAlchemy , 本质就是将以上的配置读取出来
    db.init_app(app)

    app.register_blueprint(user)

    return app
