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
    creat_table(["reader", "id_r int not null primary key auto_increment", "certificate int", "name varchar(255)",
                 "sex enum('male','female') not null", "dept int", "grade int"], cursor)


# 借书表
# attributes: 读者号 书籍号 借书日期 需要还书日期
def creat_table_record_borrow(cursor):
    creat_table(["record_borrow", "id_r_b int not null primary key auto_increment", "id_r int not null foreign key",
                 "id_book int not null foreign key", "date_borrow date", "date_return date"], cursor)


# 还书表
# attributes: 还书记录id 读者id 书籍id 借书日期 实际还书日期
def creat_table_record_return(cursor):
    creat_table(["record_return", "id_r_r int not null primary key auto_increment", "id_r int not null foreign key",
                 "id_book int not null foreign key", "date_borrow date", "date_return data"], cursor)


# 书籍表
# attributes: 书籍id 书号 书名 出版社 出版日期 作者 内容摘要
def creat_table_book(cursor):
    creat_table(["book", "id_book int not null primary key auto_increment", "book_no int not null",
                 "book_name varchar(255) not null", "publisher varchar(255)", "date_publish date",
                 "author varchar(255)", "abstract varchar(255)"], cursor)


# abstract 255 会不会有点小?


# 各种插入语句
def insert(info) -> str:

    return sql


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
    sql += "where book_no = " + book_no_s + "))"
    return select_execute(sql, cursor)


# 查询读者基本信息
# 仅支持姓名和证件号查询
def select_reader(id_r, cursor) -> tuple:
    sql = select(["*", "reader"])
    sql += "where id_r = " + id_r
    return select_execute(sql, cursor)


def select_reader_name(name, cursor) -> list:
    sql = select(["id_r", "reader"])
    sql += "where name = "+name
    ls = []
    for i in select_execute(sql, cursor):
        ls.append(select_reader(i, cursor))
    return ls


# 证件号不一定是唯一的 有可能录错了
def select_reader_certificate(certificate, cursor) -> list:
    sql = select(["id_r", "reader"])
    sql += "where certificate = " + certificate
    ls = []
    for i in select_execute(sql, cursor):
        ls.append(select_reader(i, cursor))
    return ls


# 查看读者借书信息
def select_record_borrow(id_r, cursor) -> tuple:
    sql = select(['*', 'record_borrow'])
    sql += 'where id_r = '+id_r
    return select_execute(sql, cursor)


# 查看读者还书信息
def select_record_return(id_r, cursor) -> tuple:
    sql = select(['*', 'record_return'])
    sql += 'where id_r = ' + id_r
    return select_execute(sql, cursor)


# 各种修改语句


