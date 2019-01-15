import pymysql

from webs import POOL


def create_conn():
    conn = POOL.connection()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    return conn, cursor


def close_conn(conn, cursor):
    cursor.close()
    conn.close()


def insert(my_sql, args):
    conn, cursor = create_conn()
    res = cursor.execute(my_sql, args)
    conn.commit()
    close_conn(conn, cursor)
    return res


def fetch_one(my_sql, args):
    conn, cursor = create_conn()
    cursor.execute(my_sql, args)
    res = cursor.fetchone()
    close_conn(conn, cursor)
    return res


def fetch_all(my_sql, args):
    conn, cursor = create_conn()
    cursor.execute(my_sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res


# sql = "insert into users(name,age) VALUES (%s, %s)"
#
# insert(sql, ("yao", 9))

sql = "select * from users where name=%s and age=%s"

print(fetch_one(sql, ("yao", 9)))
