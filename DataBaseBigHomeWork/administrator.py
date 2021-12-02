# -*- coding: utf-8 -*-
"""
---------------------------------------------------------
    File Name :         administrator                             
    Description :                                       
    Author :            Karl                             
    Date :              2021-12-01                          
---------------------------------------------------------
    Change Activity :   2021-12-01
    
--------------------------------------------------------- 
"""

# 定义Administrator的行为 进行封装
# 可以有多个管理员 同时在线
# 三个成员 管理员姓名 账号 密码
from database_module import *
from user import *


class Administrator(User):
    def __init__(self, name, account, cursor, db):
        super().__init__(account, cursor, db)
        self.name = name


