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
def create_database(passwd, host="localhost", user="root", dbname="liberal"):
    db = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd
    )
    cursor = db.cursor()
    cursor.execute("create database if not exists "+dbname)
    db.close()
    cursor.close()


# 连接数据库
def connect_database(passwd, host="localhost", user="root", dbname="liberal"):
    db = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
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
def creat_table(table_info, dbname="liberal"):
    [db, cursor] = connect_database(dbname)
    sql = "create table if not exists "+table_info[0]+" ("
    for i in table_info[1:]:
        sql += table_info[i]+", "
    sql += " )"
    cursor.execute(sql)
    close_connect(db, cursor)


# 读者表
# attributes: 读者号 证件号 名字 性别 系号 年级
def creat_table_reader():
    creat_table(["reader", "id_r int not null primary key auto_increment", "certificate int", "name varchar(255)",
                 "sex enum('male','female') not null", "dept int", "grade int"])


# 借书表
# attributes: 读者号 书籍号 借书日期 还书日期
def creat_table_record_borrow():
    creat_table(["record_borrow", "id_r_b int not null primary key auto_increment", "id_r int not null foreign key",
                 "id_book int not null foreign key", "date_borrow date", "date_return date"])


# 还书表
# attributes: 还书记录id 读者id 书籍id 借书日期 还书日期
def creat_table_record_return():
    creat_table(["record_return", "id_r_r int not null primary key auto_increment", "id_r int not null foreign key",
                 "id_book int not null foreign key", "date_borrow date", "date_return data"])


# 书籍表
# attributes: 书籍id 书号 书名 出版社 出版日期 作者 内容摘要
def creat_table_book():
    creat_table(["book", "id_book int not null primary key auto_increment", "book_no int not null",
                 "book_name varchar(255) not null", "publisher varchar(255)", "date_publish date",
                 "author varchar(255)", "abstract varchar(255)"])


# abstract 255 会不会有点小?


# 各种查询语句
# 查看某本书籍总数


# 查看某书当前在馆数量


# 查询读者基本信息


# 查看读者借书信息


# 各种修改语句


