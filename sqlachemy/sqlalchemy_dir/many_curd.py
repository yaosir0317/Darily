from sqlalchemy.orm import sessionmaker

from sqlalchemy_dir.many_many import engine
from sqlalchemy_dir.many_many import Book
from sqlalchemy_dir.many_many import Author


session = sessionmaker(engine)
db_session = session()


# 正向添加
book_obj = Book(name="书籍1")
book_obj.book2author = ([Author(name="作者1"), Author(name="作者2")])
db_session.add(book_obj)
db_session.commit()
db_session.close()

# 反向添加
author_obj = Author(name="作者3", author2book=[Book(name="书籍2"), Book(name="书籍3")])
db_session.add(author_obj)
db_session.commit()
db_session.close()


# 正向查询
author_list = db_session.query(Author).all()
for author in author_list:
    for book in author.author2book:
        print(book.name, author.name)


# 反向查询
book_list = db_session.query(Book).all()
for book in book_list:
    for author in book.book2author:
        print(author.name, book.name)