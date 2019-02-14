# 导入SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

# 导入数据库连接引擎
from sqlalchemy import create_engine

# 导入ORM对应数据库数据类型的字段
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

# 创建ORM模型基类
Base = declarative_base()


# 创建ORM对象
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), index=True)
    age = Column(Integer, index=True)


# 创建数据库连接
engine = create_engine("mysql+pymysql://root:@127.0.0.1:3306/db2019?charset=utf8")

# 数据库中创建User对应的表
# 去engine数据库中创建所有继承Base的ORM对象类

Base.metadata.create_all(engine)
