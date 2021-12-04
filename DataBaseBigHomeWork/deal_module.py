# -*- coding: utf-8 -*-
"""
---------------------------------------------------------
    File Name :         deal_module                             
    Description :                                       
    Author :            Karl                             
    Date :              2021-12-04                          
---------------------------------------------------------
    Change Activity :   2021-12-04
    
--------------------------------------------------------- 
"""
import json

from reader import *
from administrator import *


# info 是json格式的str
# 返回值也是一个json的str 不过内部是 list
def deal_with(data) -> str:
    info = json.loads(data)
    [db, cursor] = connect_database(info["login"])
    if info["User"] == "reader":
        user = Reader(info["id_reader"], info["account"], db, cursor)
    else:
        user = Administrator(info["name"], info["account"], db, cursor)
    ls = []
    for i in range(0, info["len"]):
        """reader"""
        if info["type"] == "borrow_book":
            ls.append(user.borrow_book())
        if info["type"] == "return_book":
            ls.append(user.return_book())
        if info["type"] == "view_info":
            ls.append(user.)
        if info["type"] == "view_record":