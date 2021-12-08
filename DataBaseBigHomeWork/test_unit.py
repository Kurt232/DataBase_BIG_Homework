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
from tkinter import *

# 初始化database

if init_library():
    print("已经初始化")
else:
    print("进行初始化")

# Administrator
[db, cursor] = connect_database(["localhost", "library", "123456"])
test_admin = Administrator("test", '123456789', db, cursor)
test_reader = Reader(1, "test", db, cursor)
test_reader2 = Reader(2, "test", db, cursor)
"""test add"""
# test_admin.add_book([1234566, "高等数学", "高等教育出版社", "2018-8-10", "同济大学", "高速退学"])
# test_admin.add_book([1234567, "线性代数", "高等教育出版社", "2018-8-10", "同济大学", "先行呆数"])
# test_admin.add_book([9787302423287, "机器学习", "清华大学出版社", "2016-1-10", "周志华", "机器学习是计算机科学领域的重要分支领域。"
#                                                                            "本书作为该领域的入门教材，在内容上尽可能涵盖机器学习基础知识的各个方面"])
# test_admin.add_reader([20201414601112, "杜云来", "male", "计算机系", "2020"])
# test_admin.add_reader([2020141461111, "杜文杰", "male", "计算机系", "2020"])
# test_admin.add_reader([2020141461112, "黎昊", "male", "软件工程系", "2020"])
# for i in test_admin.query_book(["", "", "高等教育出版社", "", "", ""]):
#    print(i)
"""Reader"""
"""借书测试"""
# test_reader.borrow_book(2, 30)
# test_reader2.borrow_book(3, 30)
# days = test_reader.borrow_book(3, 30)
# if days > 0:
#     print("有 " + str(days) + " 待还")
# else:
#     print("success")
"""还书测试"""
# days = test_reader.return_book(4, 30)
# if days > 0:
#     print("超期 " + str(days) + " 天")
# else:
#     print("未超期")
"""查看信息"""
# for i in test_reader.view_info():
#     print(i)
# for i in test_reader.view_record():
#     print(i)
# print("pass")
"""Administrator"""
# if test_admin.delete_reader(1):
#     print("success")
# else:
#     print("failure")
# if test_admin.delete_book(1):
#     print("success")
# else:
#     print("failure")
# if test_admin.delete_book(24):
#     print("success")
# else:
#     print("failure")
# for i in test_admin.query_reader(["", "", "", "", 2020]):
#     print(i)
# for i in test_admin.view_reader_record(1):
#     print(i)
# for i in test_admin.query_out_date(30):
#     print(i)
close_connect(db, cursor)

"""win test"""
# 有bug我也没办法
# info = [[["a", "a", "a", "a", "a", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"], ["b", "b", "b", "b", "b", "b"], ["c", "c", "c", "c", "c", "c"]],
#         [1, 1, 1], [2, 2, 2]]
# root = Tk()
# fr4 = Frame(root, width=600, height=300)
# fr4.grid()
# for i in range(0, 3):
#     for j in range(0, 6):
#         lbl12 = Label(fr4, width=20)
#         lbl12["text"] = info[0][i][j]
#         lbl12.grid(column=j, row=i + 1)
#     lbl13 = Label(fr4, width=20)
#     lbl13["text"] = info[1][i]
#     lbl13.grid(column=6, row=i + 1)
#     lbl14 = Label(fr4, width=20)
#     lbl14["text"] = info[2][i]
#     lbl14.grid(column=7, row=i + 1)
# # fr4.grid_forget()  # 解决
# for i in fr4.grid_info():
#     print(i)
# root.mainloop()
