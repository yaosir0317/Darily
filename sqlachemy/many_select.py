from sqlalchemy.orm import sessionmaker

from many_create import engine
from many_create import School
from many_create import Student

Session = sessionmaker(engine)
db_session = Session()

# 通过relationsh正向查询
student_list = db_session.query(Student).all()
for student in student_list:
    print(student.name, student.student2school.name)

# 通过relationship反向查询
school_list = db_session.query(School).all()
for school in school_list:
    for student in school.student2school:
        print(student.name, school.name, school.id)