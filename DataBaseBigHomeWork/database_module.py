# -*- coding: utf-8 -*-
"""
---------------------------------------------------------
    File Name :         database_module                             
    Description :                                       
    Author :            Karl                             
    Date :              2021-11-23                          
---------------------------------------------------------
    Change Activity :   2021-11-23
    
--------------------------------------------------------- 
"""
import mysql.connector


# 创建数据库
# 岂不是暴露了我的密码？
# test pass
# login is List<string>
def create_database(login, dbname="liberal"):
    db = mysql.connector.connect(
        host=login[0],
        user=login[1],
        passwd=login[2]
    )
    cursor = db.cursor()
    cursor.execute("create database if not exists "+dbname)
    db.close()
    cursor.close()


# 连接数据库
def connect_database(login, dbname="liberal"):
    db = mysql.connector.connect(
        host=login[0],
        user=login[1],
        passwd=login[2],
        database=dbname
    )
    cursor = db.cursor()
    return [db, cursor]


# 关闭与数据库的连接
def close_connect(db, cursor):
    cursor.close()
    db.close()


# 一些基本的函数
# 创建各种表
# table_info is List of string
# table_info[0] : table_name
# table_info[i] : attributes
def creat_table(table_info, cursor):
    # [db, cursor] = connect_database(dbname)
    sql = "create table if not exists "+table_info[0]+" ("
    for i in table_info[1:]:
        sql += i+", "
    sql += " )"
    cursor.execute(sql)
    # close_connect(db, cursor)


# 读者表
# attributes: 读者号 证件号 名字 性别 系号 年级
def creat_table_reader(cursor):
    creat_table(["reader", "id_reader int not null primary key auto_increment", "certificate int", "name varchar(255)",
                 "sex enum('male','female') not null", "dept varchar(255)", "grade int"], cursor)


# 借还书表
# attributes: 读者号 书籍号 借书日期 需要还书日期
def creat_table_record(cursor):
    creat_table(["record", "id_record int not null primary key auto_increment", "id_r int not null foreign key",
                 "id_book int not null foreign key", "date_borrow date", "date_return date"], cursor)


# 书籍表
# attributes: 书籍id 书号 书名 出版社 出版日期 作者 内容摘要
def creat_table_book(cursor):
    creat_table(["book", "id_book int not null primary key auto_increment", "book_no int not null",
                 "book_name varchar(255) not null", "publisher varchar(255)", "date_publish date",
                 "author varchar(255)", "abstract varchar(255)"], cursor)


# abstract 255 会不会有点小?


# 各种插入语句
def insert(info) -> str:
    sql = "(" + info[0]
    for i in info[1:]:
        sql += " ," + i
    sql += ")"
    return sql


def insert_execute(sql, db, cursor):
    cursor.execute(sql)
    db.commit()


# 插入读者表
def insert_reader(info, db, cursor):
    sql = "insert into reader (certificate, name, sex, dept, grade) values "
    sql += insert(info)
    insert_execute(sql, db, cursor)


# 插入书籍表
def insert_book(info, db, cursor):
    sql = "insert into book (book_no, book_name, publisher, date_publish, author, abstract) values "
    sql += insert(info)
    insert_execute(sql, db, cursor)


# 插入借还书表
# 还书时间无穷算出来
# 应还书时间 直接基于借书时间算
def insert_record_borrow(info, db, cursor):
    sql = "insert into record (id_reader, id_book, date_borrow, date_return) values "
    sql += insert(info)
    insert_execute(sql, db, cursor)


# 各种查询语句
# 我甚至不需要知道cursor.fetchall()返回类型 -好像是一个tuple
def select(info) -> str:
    sql = "select "+info[0]
    for i in info[1:-2]:
        sql += ", "+i
    sql += " from "+info[-1]
    return sql


def select_execute(sql, cursor) -> tuple:
    cursor.execute(sql)
    return cursor.fetchall()


# 查看某本书籍总数
def select_sum_book(book_no_s, cursor) -> tuple:
    sql = select(["count(book_no)", "book"])
    sql += "where book_no = '" + book_no_s + "'"
    return select_execute(sql, cursor)


# 查看某书当前在馆数量
# 嵌套了两层 子查询
def select_sum_book_on(book_no_s, cursor) -> tuple:
    sql = select(["count(book_no)", "book, record_borrow"])
    sql += "where not exists ( select * from record_borrow where id_r_b in"
    sql += "(" + select(["id_r_b", "book"])
    sql += "where book_no = '" + book_no_s + "'))"
    return select_execute(sql, cursor)


# 查询读者基本信息
# 调用时需要保证合法 len(info)!=0 以及内容正确
# 组合查询信息查询id
def select_reader_id(info, cursor) -> list:
    sql = select(["id_reader", "reader"])
    sql += "where " + info[0] + " = '" + info[1] + "'"
    for i in range(2, len(info), 2):
        sql += " and " + info[i] + " = '" + info[i+1] + "'"
    ls = []
    for i in select_execute(sql, cursor):
        ls.append(list(i))
    return ls


# 组合查询所以信息
def select_reader_all(info, cursor) -> list:
    sql = select(["*", "reader"])
    sql += "where " + info[0] + " = '" + info[1] + "'"
    for i in range(2, len(info), 2):
        sql += " and " + info[i] + " = '" + info[i + 1] + "'"
    ls = []
    for i in select_execute(sql, cursor):
        ls.append(list(i))
    return ls


# 查看读者借还书信息
def select_record(id_r, cursor) -> tuple:
    sql = select(['*', 'record'])
    sql += "where id_r = '" + id_r + "'"
    return select_execute(sql, cursor)


# 各种修改语句

# 各种删除语句


