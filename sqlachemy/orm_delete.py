# 想要操纵数据库 打开数据库连接
from sqlalchemy.orm import sessionmaker
# 引入创建好的连接引擎与表
from main import engine
from main import User

Session = sessionmaker(engine)
db_session = Session()

# 先查询再删除
data = db_session.query(User).filter(User.id == 1).delete()
db_session.commit()
db_session.close()
