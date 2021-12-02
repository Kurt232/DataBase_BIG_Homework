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
# attributes: 读者号 书籍号 借书日期 应还书日期 out_date(初始值为-1 正常还书为0 超期>0)
# date 按照 yyyy-mm-dd 就是字符串
def creat_table_record(cursor):
    creat_table(["record", "id_record int not null primary key auto_increment", "id_reader int not null foreign key",
                 "id_book int not null foreign key", "date_borrow date", "date_return date", "out_date int"], cursor)


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
# 完成借书手续
# 还书时间无穷算出来
# 应还书时间 直接基于借书时间算
def insert_record_borrow(info, db, cursor):
    sql = "insert into record (id_reader, id_book, date_borrow, date_return) values "
    sql += insert(info)
    insert_execute(sql, db, cursor)


# 各种查询语句
# 我甚至不需要知道cursor.fetchall()返回类型 -好像是一个tuple
# 如果是字符串 info中应该是 info = ["'name'", "'sex'"]
def select(info) -> str:
    sql = "select "+info[0]
    for i in info[1:-2]:
        sql += ", "+i
    sql += " from "+info[-1]
    return sql


def select_distinct(info) -> str:
    sql = "select distinct "+info[0]
    for i in info[1:-2]:
        sql += ", "+i
    sql += " from "+info[-1]
    return sql


def select_execute(sql, cursor) -> tuple:
    cursor.execute(sql)
    return cursor.fetchall()


# 查看某本书籍总数
def select_sum_book(book_no_s, cursor) -> int:
    sql = select(["count(book_no)", "book"])
    sql += "where book_no = " + book_no_s
    num = select_execute(sql, cursor)
    return num[0]


# 查看某书当前在馆数量
# 嵌套了两层 子查询
def select_sum_book_on(book_no_s, cursor) -> int:
    sql = select(["count(book_no)", "book, record_borrow"])
    sql += "where not exists ( select * from record_borrow where id_r_b in"
    sql += "(" + select(["id_r_b", "book"])
    sql += "where book_no = " + book_no_s + "))"
    num = select_execute(sql, cursor)
    return num[0]


# 查询读者基本信息
# 调用时需要保证合法 len(info)!=0 以及内容正确
# and 组合查询
def select_and(info) -> str:
    sql = "where " + info[0] + " = " + info[1]
    for i in range(2, len(info), 2):
        sql += " and " + info[i] + " = " + info[i+1]
    return sql


# 组合查询信息查询id
def select_reader_id(info, cursor) -> list:
    sql = select(["id_reader", "reader"])
    sql += select_and(info)
    ls = []
    for i in select_execute(sql, cursor):
        ls.append(list(i))
    return ls


# 组合查询所有读者信息 不能包含id 还需要
def select_reader_all(info, cursor) -> list:
    sql = select(["*", "reader"])
    sql += select_and(info)
    ls = []
    for i in select_execute(sql, cursor):
        ls.append(list(i))
    return ls


# info = id_reader
def select_reader(info, cursor) -> list:
    sql = select(["certificate, name, sex, dept, grade", "reader"])
    sql += "where id_reader =" + info
    return list(select_execute(sql, cursor))


# 组合查询书籍信息
def select_book_all(info, cursor) -> list:
    sql = select_distinct(["book_no, book_name, publisher, date_publish, author, abstract", "book"])
    sql += select_and(info)
    ls = []
    for i in select_execute(sql, cursor):
        ls.append(list(i))
    return ls


def select_book_id(info, cursor) -> list:
    sql = select(["id_book", "book"])
    sql += select_and(info)
    ls = []
    for i in select_execute(sql, cursor):
        ls.append(list(i))
    return ls


# 用id 查找所有 信息 用于 update_
def select_update_all_id(table, info, cursor) -> list:
    sql = select(["*", table])
    sql += "where id_" + table + " = " + info
    return list(select_execute(sql, cursor))


# 查询超期未还学生
# info = 还书期限
def select_out_date(info, cursor) -> list:
    sql = select(["*", "reader"])
    sql += "where id_reader in ("
    sql += select(["id_reader", "record"])
    sql += "where out_date = -1 and to_days(now()) - to_days(date_borrow) >= " + info
    ls = []
    for i in select_execute(sql, cursor):
        ls.append(list(i))
    return ls


# 查看某个读者是逾期
# info = [id_reader, interval]
def select_out_reader(info, cursor) -> int:
    sql = select(["count(id_reader)", "record"])
    sql += "where id_reader = " + info[0] + " and out_date = -1 and to_days(now()) - to_days(date_borrow) >= " + info
    num = select_execute(sql, cursor)  # 虽然是tuple 但是len == 1
    return num[0]


# 查看某个读者是否借书
# info = id_reader
def select_reader_is_borrow(info, cursor) -> int:
    sql = select(["count(id_reader)", "record"])
    sql += "where id_reader = " + info[0] + " and out_date = -1"
    num = select_execute(sql, cursor)  # 虽然是tuple 但是len == 1
    return num[0]


# 还书时查找对应的记录
# info = [id_reader, id_book]
# 返回 *
def select_record_to_return(info, cursor) -> list:
    sql = select(["*", "record"])
    sql += "where id_reader = " + info[0] + " and id_book = " + info[1] + " and out_date = -1"
    return list(select_execute(sql, cursor))  # 插入record表的逻辑确定了 只能返回一条记录


# 查看读者借还书信息 未还书在上面 升序
# info = id_reader
def select_record(info, cursor) -> list:
    sql = select(['*', 'record order by out_date '])
    sql += "where id_reader = " + info + ""
    return list(select_execute(sql, cursor))


# info id_book
def select_book_off(info, cursor) -> bool:
    sql = select(["out_date", "record"])
    sql += "where id_book = " + info
    return select_execute(sql, cursor)[0] != -1  # 约束规定了 返回值是一个长度为1的元组


# 各种修改语句
def update_execute(sql, db, cursor):
    cursor.execute(sql)
    db.commit()


# 修改书籍基本信息
# 约束交给调用它的函数
# attribute 是指各个属性 attribute[0] 是主键 attribute = list[str, str ...]
# 按照book_id来修改 这样最稳妥 更新界面设置成 展示 原始数据 然后 在原来的基础上更新 所以 info 是所有数据
def update(table, attribute, info, db, cursor):
    sql = "update " + table + " set"
    for i in range(1, len(attribute)):
        sql += " " + attribute[i] + " = " + info[i]
    sql += "where " + attribute[0] + " = " + info[0]  # 没有修改id
    update_execute(sql, db, cursor)


# 更新读者信息
def update_reader(attribute_reader, info, db, cursor):
    update(table="reader", attribute=attribute_reader, info=info, db=db, cursor=cursor)


# 更新书籍信息
def update_book(attribute_book, info, db, cursor):
    update(table="book", attribute=attribute_book, info=info, db=db, cursor=cursor)


# 更新借还书表
# 即完成还书手续
def update_record(attribute_book, info, db, cursor):
    update(table="record", attribute=attribute_book, info=info, db=db, cursor=cursor)


# 各种删除语句
# 检查删除条件
# 使用时保证info的正确性 info[attribute, value]
def delete_check(info, cursor) -> bool:
    sql = select([info[0], "record"])
    sql += "where " + info[0] + " = " + info[1] + " and out_date = -1 "
    result = select_execute(sql, cursor)  # info 的正确性保证 result = (info[0],) or result = (,)
    return len(result) == 0


# 删除已有数据
def delete(table, info, db, cursor):
    sql = "delete from " + table + "where " + info[0] + " = " + info[1]
    cursor.execute(sql)
    db.commit()


# 删除已有记录 record 为后面做准备
def delete_record(info, db, cursor):
    delete(table="record", info=info, db=db, cursor=cursor)


# 删除已有书籍
def delete_book(id_book, db, cursor):
    if delete_check(["id_book", id_book], cursor):
        delete_record(info=["id_book", id_book], db=db, cursor=cursor)
        delete(table="book", info=["id_book", id_book], db=db, cursor=cursor)


# 删除已有成员
def delete_reader(id_reader, db, cursor):
    if delete_check(["id_reader", id_reader], cursor):
        delete_record(info=["id_reader", id_reader], db=db, cursor=cursor)
        delete(table="reader", info=["id_reader", id_reader], db=db, cursor=cursor)
