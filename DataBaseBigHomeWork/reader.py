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
import datetime

from database_module import *
from user import *
from datetime import date, timedelta


class Reader(User):
    def __init__(self, reader_id, account, cursor, db):
        super().__init__(account, cursor, db)
        self.id = reader_id

    # 借书的时候用book_id借 interval是还书间隔
    # 见图(上级界面负责控制)
    # 如失败 发出信息 借书失败，有x本超期未还书籍 返回x
    # 成功是返回0发出消息
    def borrow_book(self, id_book, interval) -> int:
        num = select_out_reader([self.id, interval], self.cursor)
        if num > 0:
            return num
        now = date.today()
        date_borrow = now.isoformat()
        insert_record_borrow([self.id, id_book, "'" + date_borrow + "'", -1], self.db, self.cursor)
        return num

    def return_book(self, id_book, interval) -> int:
        attribute = ["id_record", "id_reader", "id_book", "date_borrow", "date_return", "out_date"]
        ls = select_record_to_return([self.id, id_book], self.cursor)
        # 这边要算算时间
        now = date.today()  # date
        date_borrow = date.fromisoformat(ls[3])  # date
        date_return = now.isoformat()  # str
        # timedelta 类
        delta = now - date_borrow  # timedelta
        beta = delta.days - interval  # int
        if beta <= 0:
            beta = 0  # 返回 0 在正常时间内还书
        ls[4] = "'" + date_return + "'"  # date_return
        ls[5] = beta  # out_date
        # 还书
        update_record(attribute, ls, self.db, self.cursor)
        return beta





