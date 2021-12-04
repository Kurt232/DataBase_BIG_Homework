# -*- coding: utf-8 -*-
"""
---------------------------------------------------------
    File Name :         window                             
    Description :                                       
    Author :            Karl                             
    Date :              2021-12-04                          
---------------------------------------------------------
    Change Activity :   2021-12-04
    
--------------------------------------------------------- 
"""
from tkinter import *
from tkinter import ttk
"""reader"""


# 登录界面
# 返回一个json字符串
def login(title) -> str:
    root = Tk()
    root.geometry("400x300")
    root.title(title)
    # label
    describe = Label(root, width=40, height=2, text="请读者在以下输入账号和密码", font=('楷体', 10))
    describe.grid(column=0, row=0)
    account = Label(root, width=10, height=2, test="account:", font=('楷体', 10))
    account.grid(column=0, row=1)
    password = Label(root, width=10, height=2, test="password:", font=('楷体', 10))
    password.grid(column=0, row=2)
    root.mainloop()
    return title


login("Reader")
