# 想要操纵数据库 打开数据库连接
from sqlalchemy.orm import sessionmaker
# 引入创建好的连接引擎与表
from sqlalchemy_dir.main import engine
from sqlalchemy_dir.main import User

Session = sessionmaker(engine)
db_session = Session()

# 修改数据即先查找再修改
data = db_session.query(User).filter(User.id == 1).update({"name": "yaoshao"})
db_session.commit()
db_session.close()

# 在原有值基础上添加
db_session.query(User).filter(User.id > 0).update({User.name: User.name + "99"}, synchronize_session=False)