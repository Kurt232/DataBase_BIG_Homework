# -*- coding: utf-8 -*-
"""
---------------------------------------------------------
    File Name :         test                             
    Description :                                       
    Author :            Karl                             
    Date :              2021-11-09                          
---------------------------------------------------------
    Change Activity :   2021-11-23
    
--------------------------------------------------------- 
"""
from database_module import *
import json


# 返回是否进行初始化
# pass test
def init_library() -> bool:
    with open("regedit.json", "r", encoding="utf-8") as fp:
        json_data = json.load(fp)
        fp.close()
    if json_data["register"]:
        return True
    json_data["register"] = True
    with open("regedit.json", "w", encoding="utf-8") as fp:
        json.dump(json_data, fp)
        fp.close()
    create_database(json_data["login"])
    [db, cursor] = connect_database(json_data["login"])
    create_table_reader(cursor)
    create_table_book(cursor)
    create_table_record(cursor)
    close_connect(db, cursor)
    return False
