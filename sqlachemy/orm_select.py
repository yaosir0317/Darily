# 想要操纵数据库 打开数据库连接
from sqlalchemy.orm import sessionmaker
# 引入创建好的连接引擎与表
from main import engine
from main import User

Session = sessionmaker(engine)
db_session = Session()

# # 简单查询
# user_list = db_session.query(User).all()
# for user in user_list:
#     print(user.name, user.age)
#
# user = db_session.query(User).first()
# print(user.name, user.age)
#
# # 带条件的查询
# user_list = db_session.query(User).filter(User.id == 1).all()
# print(user_list[0].name, user_list[0].age)
#
# user = db_session.query(User).filter_by(id=1).first()
# print(user.name, user.age)
#
# user_list = db_session.query(User).filter(User.id <= 2).all()
# for user in user_list:
#     print(user.name, user.age)
#
# # 查看查询的sql语句
# sql = db_session.query(User).filter(User.id >= 2)
# print(sql)

# 高级查询
# and or

# from sqlalchemy.sql import and_
# from sqlalchemy.sql import or_
# user_list1 = db_session.query(User).filter(and_(User.id >= 2, User.age >= 20)).all()
# user_list2 = db_session.query(User).filter(or_(User.id >= 2, User.age >= 20)).all()


# # 查询数据 指定查询数据列 加入别名
# r2 = db_session.query(User.name.label('username'), User.id).first()
# # 此时r2.name的别名为r2.username, r2.name就不能再使用了
# print(r2.id, r2.username)

# 原生SQL筛选条件
from sqlalchemy.sql import text
# r7 = db_session.query(User).from_statement(text("SELECT * FROM User where name=:name")).params(name='y1').all()
# print(r7[0].name)

# 字符串匹配方式筛选条件 并使用 order_by进行排序
r6 = db_session.query(User).filter(text("id<:value and name=:name")).params(value=224, name='DragonFire').order_by(User.id).all()

# query的时候我们不在使用User ORM对象,而是使用User.name来对内容进行选取
user_list = db_session.query(User.name).all()