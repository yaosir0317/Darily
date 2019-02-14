# 想要操纵数据库 打开数据库连接
from sqlalchemy.orm import sessionmaker
# 引入创建好的连接引擎
from main import engine
from main import User


# 创建会话窗口
Session = sessionmaker(engine)
# 打开会话窗口
db_session = Session()

# # 增加单条数据
# user_obj = User(name="yao", age=18)
# # 通过打开的会话窗口提交数据
# db_session.add(user_obj)
# # 执行会话窗口的操作
# db_session.commit()
# # 关闭会话窗口
# db_session.close()

db_session.add_all([
    User(name="y1", age=19),
    User(name="y2", age=20),
    User(name="y3", age=21)
])
# 执行会话窗口的操作
db_session.commit()
# 关闭会话窗口
db_session.close()
