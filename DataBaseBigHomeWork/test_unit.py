# -*- coding: utf-8 -*-
"""
---------------------------------------------------------
    File Name :         test_unit                             
    Description :                                       
    Author :            Karl                             
    Date :              2021-12-01                          
---------------------------------------------------------
    Change Activity :   2021-12-01
    
--------------------------------------------------------- 
"""
from init_library import init_library
from administrator import *
from reader import *

# 初始化database

if init_library():
    print("已经初始化")
else:
    print("进行初始化")

# Administrator
[db, cursor] = connect_database(["localhost", "library", "123456"])
test_admin = Administrator("test", '123456789', db, cursor)
# test_admin.add_book([1234566, "高等数学", "高等教育出版社", "2018-8-10", "同济大学", "高速退学"])
# test_admin.add_book([1234567, "线性代数", "高等教育出版社", "2018-8-10", "同济大学", "先行呆数"])
# test_admin.add_reader([20201414601112, "杜云来", "male", "计算机系", "2020"])
# test_admin.add_book([9787302423287, "机器学习", "清华大学出版社", "2016-1-10", "周志华", "机器学习是计算机科学领域的重要分支领域。"
#                                                                           "本书作为该领域的入门教材，在内容上尽可能涵盖机器学习基础知识的各个方面"])
# test_admin.add_reader([2020141461111, "杜文杰", "male", "计算机系", "2020"])
# test_admin.add_reader([2020141461112, "黎昊", "male", "软件工程系", "2020"])
test_reader = Reader('1', "test", cursor, db)


