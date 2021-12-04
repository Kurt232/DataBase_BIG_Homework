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
        """user"""
        if info["type"] == "query_book":
            ls.append(user.query_book(info["info"]))
        """reader"""
        if info["type"] == "borrow_book":
            ls.append(user.borrow_book(info["id_book"], info["interval"]))
        if info["type"] == "return_book":
            ls.append(user.return_book(info["id_record"], info["interval"]))
        if info["type"] == "view_info":
            ls.append(user.view_info())
        if info["type"] == "view_record":
            ls.append(user.view_record())
        """admin"""
        if info["type"] == "add_book":
            ls.append(user.add_book(info["info"]))
        if info["type"] == "add_reader":
            ls.append(user.add_reader(info["info"]))
        if info["type"] == "delete_book":
            ls.append(user.delete_book(info["info"]))
        if info["type"] == "delete_reader":
            ls.append(user.delete_reader(info["info"]))
        if info["type"] == "update_book":
            ls.append(user.update_book(info["info"]))
        if info["type"] == "update_reader":
            ls.append(user.update_reader(info["info"]))
        if info["type"] == "query_reader":
            ls.append(user.query_reader(info["info"]))
        if info["type"] == "view_reader_info":
            ls.append(user.view_reader_info(info["info"]))
        if info["type"] == "view_reader_record":
            ls.append(user.view_reader_record(info["info"]))
        if info["type"] == "query_out_date":
            ls.append(user.query_out_date(info["interval"]))
    return json.dumps(ls)

                                        