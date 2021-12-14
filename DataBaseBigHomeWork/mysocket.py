# -*- coding: utf-8 -*-
"""
---------------------------------------------------------
    File Name :         mysocket
    Description :                                       
    Author :            Karl                             
    Date :              2021-12-04                          
---------------------------------------------------------
    Change Activity :   2021-12-04
    
--------------------------------------------------------- 
"""

import socket
from multiprocessing import *
from reader import *
from administrator import *
import json


# 返回类型是一个json字符串 内容: id_reader account
# data ::= [[id_reader, "account", "password"],]
# { info : [id_reader, "account", "password"]}
def login_check_reader(info) -> str:
    id_reader = 0
    account = ""
    with open(r"C:\Users\Karl\Desktop\Python\DataBaseBigHomeWork\login_reader.json", "r", encoding="utf-8") as fp:
        json_data = json.load(fp)
        fp.close()
    flag = False
    for i in json_data:
        if info["account"] == i[1] and info["password"] == i[2]:
            id_reader = i[0]
            account = info["account"]
            flag = True
            break
    if flag:
        send = {"user": "reader", "id_reader": id_reader, "account": account, "port": 7777}
        return json.dumps(send)
    else:
        return ""


# { info : ["name", "account", "password"]}
# login_admin.json
# [["name", "account", "password"],]
def login_check_admin(info) -> str:
    name = ""
    account = ""
    with open(r"C:\Users\Karl\Desktop\Python\DataBaseBigHomeWork\login_admin.json", "r", encoding="utf-8") as fp:
        json_data = json.load(fp)
        fp.close()
    flag = False
    for i in json_data:
        if info["account"] == i[1] and info["password"] == i[2]:
            name = i[0]
            account = info["account"]
            flag = True
            break
    if flag:
        send = {"user": "admin", "name": name, "account": account, "port": 7777}
        return json.dumps(send)
    else:
        return ""


# 以json字符串形式返回
def socket_client(info: str, port: int) -> str:
    address = ('192.168.1.101', port)  # 服务端地址和端口
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # noinspection PyBroadException
        try:
            s.connect(address)  # 尝试连接服务端
        except Exception:
            return '404'
        s.sendall(info.encode())
        data = s.recv(1024)
        data = data.decode()
        s.close()
    return data


# 涉及到端口的得到和释放
# 尝试用多进程来解决
def socket_service(port=8888):
    address = ('192.168.1.101', port)  # 服务端地址和端口
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(address)  # 绑定服务端地址和端口
        s.listen(5)  # listen 的消息数量为 5
        while True:
            conn, addr = s.accept()  # 返回客户端地址和一个新的 socket 连接
            data = conn.recv(1024)  # buffer_size 等于 1024
            info = json.loads(data.decode())
            # 默认在端口号+1 的场景下工作 多进程程
            if data:
                if info["user"] == "admin":
                    msg = login_check_admin(info)  # 进行登录检查
                elif info["user"] == "reader":
                    msg = login_check_reader(info)
                if msg:  # msg 非空 登录成功
                    conn.sendall(msg.encode())
                else:
                    conn.sendall("failure".encode())
            conn.close()


# info 是json格式的str
# 返回值也是一个json的str 不过内部是 list
def deal_with(conn):
    db, cursor = connect_database(["localhost", "library", "123456"])
    data = conn.recv(1024)
    info = json.loads(data.decode())
    if info["user"] == "reader":
        user = Reader(info["id_reader"], info["account"], db, cursor)
    else:
        user = Administrator(info["name"], info["account"], db, cursor)
    ls = []
    # noinspection PyBroadException
    try:
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
                user.add_reader(info["info"])
                ls.append(user.query_reader(info["info"])[0][0])  # 返回id_reader
                with open(r"C:\Users\Karl\Desktop\Python\DataBaseBigHomeWork\login_reader.json", "r+") as fp:
                    data: list = json.load(fp)
                    data.append({"account": str(ls[0]), "password": 123456})
                    json.dump(data, fp)
                    fp.close()
                # 写日志
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
            if info["type"] == "record_reader":
                ls.append(user.view_reader_record(info["info"]))
            if info["type"] == "record_book":
                ls.append(user.view_reader_record(info["info"]))  # 要改
            if info["type"] == "query_out_date":
                ls.append(user.query_out_date(info["interval"]))
    except Exception:
        conn.sendall("failure".encode())
        conn.close()
    if conn:
        if not ls:
            conn.sendall("failure".encode())
        else:
            conn.sendall(json.dumps(ls).encode())
        conn.close()


def socket_execute(port, lock):
    address = ('192.168.1.101', port)  # 服务端地址和端口
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(address)  # 绑定服务端地址和端口
        s.listen(5)  # listen 的消息数量为 5
        while True:
            conn, addr = s.accept()  # 返回客户端地址和一个新的 socket 连接
            if __name__ == '__main__':
                p = Process(target=deal_with, args=(conn, lock))
                p.start()
            conn.close()
