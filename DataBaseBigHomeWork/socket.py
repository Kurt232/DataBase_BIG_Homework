# -*- coding: utf-8 -*-
"""
---------------------------------------------------------
    File Name :         socket
    Description :                                       
    Author :            Karl                             
    Date :              2021-12-04                          
---------------------------------------------------------
    Change Activity :   2021-12-04
    
--------------------------------------------------------- 
"""
import json
import socket

from deal_module import *
from multiprocessing import *


# 返回类型是一个json字符串 内容: id_reader account
# data = "{ "account" : "x", "password" : "x"}"
# { info : [id_reader, "account", "password"]}
def login_check_reader(data) -> str:
    id_reader = 0
    account =""
    with open("login_reader.json", "r", encoding="utf-8") as fp:
        json_data = json.load(fp)
        fp.close()
    info = json.loads(data)
    flag = False
    for i in json_data:
        if info["account"] == i["info"][1] and info["password"] == i["info"][2]:
            id_reader = i["info"][0]
            account = info["account"]
            flag = True
            break
    if flag:
        with open("regedit.json", "r", encoding="utf-8") as fp:
            json_data = json.load(fp)
            fp.close()
        send = {"id_reader": id_reader, "account": account, "login": json_data["login"]}
        return json.dumps(send)
    else:
        return ""


# { info : ["name", "account", "password"]}
def login_check_admin(data) -> str:
    name = ""
    account = ""
    with open("login_admin.json", "r", encoding="utf-8") as fp:
        json_data = json.load(fp)
        fp.close()
    info = json.loads(data)
    flag = False
    for i in json_data:
        if info["account"] == i["info"][1] and info["password"] == i["info"][2]:
            name = i["info"][0]
            account = info["account"]
            flag = True
            break
    if flag:
        with open("regedit.json", "r", encoding="utf-8") as fp:
            json_data = json.load(fp)
            fp.close()
        send = {"name": name, "account": account, "login": json_data["login"]}
        return json.dumps(send)
    else:
        return ""


# 以json字符串形式返回
def socket_client(info, port) -> str:
    address = ('192.168.1.108', port)  # 服务端地址和端口
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # noinspection PyBroadException
        try:
            s.connect(address)  # 尝试连接服务端
        except Exception:
            return '404'
        s.sendall(info)
        data = s.recv(1024)
        data = data.decode()
        s.close()
    return data


# 涉及到端口的得到和释放
# 尝试用多进程来解决
def socket_service(info=False, port=8888):
    address = ('192.168.1.108', port)  # 服务端地址和端口
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(address)  # 绑定服务端地址和端口
        s.listen(5)  # listen 的消息数量为 5
        conn, addr = s.accept()  # 返回客户端地址和一个新的 socket 连接
        print('[+] Connected with', addr)
        with conn:
            while True:
                data = conn.recv(1024)  # buffer_size 等于 1024
                data = data.decode()
                if info:
                    # 默认在端口号+1 的场景下工作 多进程程
                    if not data:
                        break
                    msg = login_check_reader(data)  # 进行登录检查
                    if msg:  # msg 非空 登录成功
                        conn.sendall(str(port+1))
                        if __name__ == '__main__':
                            p = Process(target=socket_service(port=port+1), args=('Python',))
                            p.start()
                    else:
                        conn.sendall("failure")
                else:
                    conn.sendall(deal_with(data))
                    break
            conn.close()
            s.close()

