from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship

Base = declarative_base()


class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), index=True)
    school_id = Column(Integer, ForeignKey("school.id"))
    student2school = relationship("School", backref="student2school")


class School(Base):
    __tablename__ = "school"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))


engine = create_engine("mysql+pymysql://root:@127.0.0.1:3306/db2019?charset=utf8")
Base.metadata.create_all(engine)
