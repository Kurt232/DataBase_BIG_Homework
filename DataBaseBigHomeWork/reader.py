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
        date = str(datetime.datetime.now()).split(" ")[0]
        insert_record_borrow([self.id, id_book, "'" + date + "'", -1], self.db, self.cursor)
        return num



