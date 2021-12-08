# -*- coding: utf-8 -*-
"""
---------------------------------------------------------
    File Name :         client_reader
    Description :                                       
    Author :            Karl                             
    Date :              2021-12-04                          
---------------------------------------------------------
    Change Activity :   2021-12-04
    
--------------------------------------------------------- 
"""
from tkinter import *
from tkinter import messagebox
import tkinter as tk
from mysocket import *
import json

"""reader"""


def check_login():
    global flag
    global port
    info = {"account": E_account.get(), "password": E_password.get()}
    data = json.dumps(info)
    port = socket_client(data, 8888)
    if port == "404":
        messagebox.showerror(title="警告", message="与服务器未连接")
    elif port == "failure":
        messagebox.showinfo(title="错误", message="账号或密码错误")
    else:
        messagebox.showinfo(title="信息", message="登录成功")
        flag = True


def book_query():
    if port == 8888:
        messagebox.showerror(title="警告", message="还未登录")
    else:
        fr4.grid_forget()
        fr4.grid()
        lbl4.grid(column=0, row=0)
        lbl5.grid(column=1, row=0)
        lbl6.grid(column=0, row=2)
        lbl7.grid(column=1, row=2)
        lbl8.grid(column=0, row=4)
        lbl9.grid(column=1, row=4)
        ety0.grid(column=0, row=1)
        ety1.grid(column=1, row=1)
        ety2.grid(column=0, row=3)
        ety3.grid(column=1, row=3)
        ety4.grid(column=0, row=5)
        ety5.grid(column=1, row=5)
        button_query.grid(column=1, row=6)


def send_query():
    global port
    if port == 8888:
        messagebox.showerror(title="警告", message="还未登录")
    else:
        ls = [ety0.get(), ety1.get(), ety2.get(), ety3.get(), ety4.get(), ety5.get()]
        data = {"type": "query_book", "info": ls}
        data_json = json.dumps(data)
        # 返回查询到的信息
        feedback = socket_client(data_json, port)
        if feedback == "404":
            messagebox.showwarning(title="警告", message="登录已过期， 请重新登录")
            port = 8888
        else:
            fr4.grid_forget()
            info: list = json.loads(feedback)
            lbl11.grid(column=1, row=0)
            lbl10.grid(column=0, row=0)
            lbl4.grid(column=2, row=0)
            lbl5.grid(column=3, row=0)
            lbl6.grid(column=4, row=0)
            lbl7.grid(column=5, row=0)
            lbl8.grid(column=6, row=0)
            lbl9.grid(column=7, row=0)
            for i in range(0, len(info[0])):
                for j in range(0, 6):
                    lbl12 = Label(fr4, width=20)
                    lbl12["text"] = info[0][i][j]
                    lbl12.grid(column=j, row=i+1)
                lbl13 = Label(fr4, width=20)
                lbl13["text"] = info[1][i]
                lbl13.grid(column=6, row=i+1)
                lbl14 = Label(fr4, width=20)
                lbl14["text"] = info[2][i]
                lbl14.grid(column=7, row=i+1)


# id_reader都在服务器上
def query_reader():
    global port
    if port == 8888:
        messagebox.showerror(title="警告", message="还未登录")
    else:
        fr4.grid_forget()
        lbl15.grid(column=0, row=0)
        lbl16.grid(column=1, row=0)
        lbl17.grid(column=2, row=0)
        lbl18.grid(column=3, row=0)
        lbl19.grid(column=4, row=0)
        data = {"type": "view_info"}
        data_json = json.dumps(data)
        feedback = socket_client(data_json, port)
        if feedback == "404":
            messagebox.showwarning(title="警告", message="登录已过期， 请重新登录")
            port = 8888
        else:
            info = json.loads(feedback)
            for i in range(0, 5):
                lbl20 = Label(fr4, width=20)
                lbl20["text"] = info[i]
                lbl20.grid(column=i, row=1)


def record_query():
    global port
    if port == 8888:
        messagebox.showerror(title="警告", message="还未登录")
    else:
        fr4.grid_forget()
        lbl21.grid(column=0, row=0)
        lbl22.grid(column=1, row=0)
        lbl23.grid(column=2, row=0)
        lbl24.grid(column=3, row=0)
        lbl25.grid(column=4, row=0)
        data = {"type": "view_record"}
        data_json = json.dumps(data)
        feedback = socket_client(data_json, port)
        if feedback == "404":
            messagebox.showwarning(title="警告", message="登录已过期， 请重新登录")
            port = 8888
        else:
            info = json.loads(feedback)
            for i in range(0, 5):
                lbl26 = Label(fr4, width=20)
                lbl26["text"] = info[i]
                lbl26.grid(column=i, row=1)


# 登录界面
# 返回一个json字符串
root = Tk()
root.title("图书馆读者系统")
# global
flag = False
port = 8888
# 背景
photo = PhotoImage(file="assert/img.png")
fr0 = Frame(root, width=400, height=225)
fr0.grid(column=0, row=0)
background = Label(fr0, image=photo, width=400, height=225)
background.grid(column=0, row=0)
# 登录
fr1 = Frame(root, width=600, height=225)
fr1.grid(column=1, row=0)
L_login = Label(fr1, text="读者登录", font=("华文行楷", 30))
L_login.grid(column=0, row=0)
L_account = Label(fr1, text="账户:")
L_account.grid(column=0, row=1)
E_account = Entry(fr1, bd=10)
E_account.grid(column=1, row=1)
L_password = Label(fr1, text="密码:")
L_password.grid(column=0, row=2)
E_password = Entry(fr1, bd=10)
E_password.grid(column=1, row=2)
log_in = Button(fr1, text="login", command=lambda: check_login(), bg="green", width=10)
log_in.grid(column=0, row=3)
log_quit = Button(fr1, text="quit", command=lambda: sys.exit(0), bg="red", width=10)
log_quit.grid(column=1, row=3)
# 功能
fr2 = Frame(root, width=400, height=300)
fr2.grid(column=0, row=1)
fr3 = Frame(root, width=600, height=300)
fr3.grid(column=1, row=1)
Lbl1 = Label(fr2, text="菜单", font=("Arial", 30))
Lbl1.grid(column=0, row=0)
# 查书 查到后点开 刷新后 再点书籍可以借书
lbl2 = Label(fr2, text="点击书籍详情进行借书")
lbl2.grid(column=1, row=1)
query_book = Button(fr2, text="查询书籍", command=book_query, width=10)
query_book.grid(column=0, row=1)
fr4 = Frame(fr3, width=600, height=300)
lbl4 = Label(fr4, text="书号:")
lbl5 = Label(fr4, text="书名:")
lbl6 = Label(fr4, text="出版社:")
lbl7 = Label(fr4, text="出版日期:")
lbl8 = Label(fr4, text="作者:")
lbl9 = Label(fr4, text="内容摘要:")
ety0 = Entry(fr4, bd=10)
ety1 = Entry(fr4, bd=10)
ety2 = Entry(fr4, bd=10)
ety3 = Entry(fr4, bd=10)
ety4 = Entry(fr4, bd=10)
ety5 = Entry(fr4, bd=10)
button_query = Button(fr4, text="查询", command=send_query, width=10, fg="green")
# 展示书籍信息 弄一个框框
lbl10 = Label(fr4, text="书籍总数")
lbl11 = Label(fr4, text="在馆数量")
# 个人信息
query_info = Button(fr2, text="个人信息", width=10, command=query_reader)
query_info.grid(column=0, row=2)
lbl3 = Label(fr2, text="点击查看个人信息")
lbl3.grid(column=1, row=2)
# 自己应该可以修改
lbl15 = Label(fr4, text="证件号")
lbl16 = Label(fr4, text="名字")
lbl17 = Label(fr4, text="性别")
lbl18 = Label(fr4, text="系号")
lbl19 = Label(fr4, text="年级")

# 借还书情况 点击书籍 进行还书
query_record = Button(fr2, text="借还书情况", width=10, command=record_query)
query_record.grid(column=0, row=3)
lbl3 = Label(fr2, text="点击待还书籍信息，进行还书")
lbl3.grid(column=1, row=3)
lbl21 = Label(fr4, text="记录号")
lbl22 = Label(fr4, text="书名")  # 需要处理 放在服务器端处理算了
lbl23 = Label(fr4, text="借书日期")
lbl24 = Label(fr4, text="还书日期")
lbl25 = Label(fr4, text="超期天数")
# 关闭窗口后终止程序
# 功能显示区

root.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))
root.mainloop()
