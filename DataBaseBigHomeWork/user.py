# -*- coding: utf-8 -*-
"""
---------------------------------------------------------
    File Name :         user                             
    Description :                                       
    Author :            Karl                             
    Date :              2021-12-01                          
---------------------------------------------------------
    Change Activity :   2021-12-01
    
--------------------------------------------------------- 
"""

# 定义user的行为
# 两个成员 account password
from database_module import *


class User:
    # 用户登录 由上级函数控制 登录函数
    # cursor 是数据库的指针
    def __init__(self, account, db, cursor):
        self.account = account
        self.cursor = cursor
        self.db = db

    # info 的约定如下 长度为 6
    # 包括：书号、书名、出版社、出版日期、作者、内容摘要
    # 若为空 用 "" 标注
    # 输出的时候是三列 书籍信息 总数 在馆数量
    def query_book(self, info) -> list:
        attribute_book = ["id_book", "book_no", "book_name", "publisher", "date_publish", "author", "book"]
        info1 = []
        ls_info = []
        ls_sum = []
        ls_on = []
        for i in range(0, 6):
            if info[i] != "":
                info1.append(attribute_book[i+1])
                if isinstance(info[i], str):
                    info1.append("'" + info[i] + "'")
                else:
                    info1.append(info[i])
        length = len(info1)
        if length == 0:
            return []
        ls_info.extend(select_book_all(info=info1, cursor=self.cursor))
        for i in range(0, length):
            # info[i][0] 是 book_no
            ls_sum.append(select_sum_book(book_no_s=ls_info[i][0], cursor=self.cursor))
            ls_on.append(select_sum_book_on(book_no_s=ls_info[i][0], cursor=self.cursor))
        return [*ls_info, *ls_sum, *ls_on]  # 语法糖
