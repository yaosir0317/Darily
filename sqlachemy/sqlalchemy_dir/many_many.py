from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship


Base = declarative_base()


class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))
    book2author = relationship("Author", secondary="relation", backref="author2book")


class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))


class Relation(Base):
    __tablename__ = "relation"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("book.id"))
    author_id = Column(Integer, ForeignKey("author.id"))


engine = create_engine("mysql+pymysql://root:@127.0.0.1:3306/db2019?charset=utf8")
Base.metadata.create_all(engine)
