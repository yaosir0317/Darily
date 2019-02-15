from sqlalchemy.orm import sessionmaker

from sqlalchemy_dir.many_create import engine
from sqlalchemy_dir.many_create import School
from sqlalchemy_dir.many_create import Student

Session = sessionmaker(engine)
db_session = Session()

sch = db_session.query(School).filter(School.name == "123").first()
stu = db_session.query(Student).filter(Student.name == "yaoshao").update({"school_id": sch.id})
db_session.commit()
db_session.close()