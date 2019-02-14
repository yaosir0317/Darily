from sqlalchemy.orm import sessionmaker

from many_create import engine
from many_create import School
from many_create import Student

Session = sessionmaker(engine)
db_session = Session()

# 添加数据
sch_obj = School(name="家里蹲")
db_session.add(sch_obj)
db_session.commit()

school = db_session.query(School).filter(School.name == "家里蹲").first()
stu_obj = Student(name="yao", school_id=school.id)
db_session.add(stu_obj)
db_session.commit()
db_session.close()

# 通过relationshi正向添加
stu_obj = Student(name="yaoshao", student2school=School(name="蹲家里"))
db_session.add(stu_obj)
db_session.commit()
db_session.close()

# 通过relationship反向添加
sch_obj = School(name="蹲")
sch_obj.student2school = [Student(name="y1"), Student(name="y2")]
db_session.add(sch_obj)
db_session.commit()
db_session.close()
