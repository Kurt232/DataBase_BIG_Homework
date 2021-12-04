# -*- coding: utf-8 -*-
"""
---------------------------------------------------------
    File Name :         reader                             
    Description :                                       
    Author :            Karl                             
    Date :              2021-12-01                          
---------------------------------------------------------
    Change Activity :   2021-12-01
    
--------------------------------------------------------- 
"""

# 定义reader的行为 这里需要异常处理

from user import *
from datetime import date, timedelta
from database_module import *


class Reader(User):
    def __init__(self, id_reader, account, db, cursor):
        super().__init__(account, db, cursor)
        self.id = id_reader

    # pass test
    # 借书的时候用book_id借 interval是还书间隔
    # 见图(上级界面负责控制)
    # 如失败 发出信息 借书失败，有x本超期未还书籍 返回x
    # 成功是返回0发出消息
    # 不会出现 把一本不在库中的书借走 由上级界面控制
    def borrow_book(self, id_book, interval) -> int:
        num = select_out_reader([str(self.id), str(interval)], self.cursor)
        if num > 0:
            return num
        now = date.today()
        date_borrow = now.isoformat()
        insert_record_borrow([str(self.id), str(id_book), "'" + str(date_borrow) + "'", "null", '-1'], self.db, self.cursor)
        return num

    def return_book(self, id_record, interval) -> int:
        attribute = ["id_record", "id_reader", "id_book", "date_borrow", "date_return", "out_date"]
        ls = select_record(str(id_record), self.cursor)
        # 这边要算算时间
        now = date.today()  # date
        date_borrow = ls[3]  # date
        # timedelta 类
        delta = now - date_borrow  # timedelta
        beta = delta.days - interval  # int
        if beta <= 0:
            beta = 0  # 返回 0 在正常时间内还书
        ls[3] = date_borrow.isoformat()  # str
        ls[4] = now.isoformat()  # date_return
        ls[5] = beta  # out_date
        # 还书
        update_record(attribute, process_list(ls), self.db, self.cursor)
        return beta

    # pass test
    # 返回内容 [0]是id_reader
    def view_info(self) -> list:
        return select_reader(str(self.id), self.cursor)

    # pass test
    # 未还书的记录再上面，上级界面检测到 out_date为-1即不显示即可
    def view_record(self) -> list:
        return select_record(str(self.id), self.cursor)




