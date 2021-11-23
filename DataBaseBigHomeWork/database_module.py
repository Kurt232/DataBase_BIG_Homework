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
def create_database(dbname="liberal"):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="180014"
    )
    cursor = db.cursor()
    cursor.execute("create database if not exists "+dbname)
    db.close()
    cursor.close()


# 连接数据库
def connect_database(dbname="liberal"):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="180014",
        database=dbname
    )
    cursor = db.cursor()
    return [db, cursor]


# 关闭与数据库的连接
def close_connect(db, cursor):
    cursor.close()
    db.close()


# 创建各种表
def creat_table(table_name, dbname="liberal"):
    [db, cursor] = connect_database(dbname)
    cursor.execute("create tables if not exists "+table_name)
    close_connect(db, cursor)

# 各种查询语句


# 各种修改语句


