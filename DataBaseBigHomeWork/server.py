# -*- coding: utf-8 -*-
"""
---------------------------------------------------------
    File Name :         server_admin                             
    Description :                                       
    Author :            Karl                             
    Date :              2021-12-11                          
---------------------------------------------------------
    Change Activity :   2021-12-11
    
--------------------------------------------------------- 
"""

import sys
from mysocket import *
from multiprocessing import Process, Lock
import json


class Server:

    def __init__(self):
        self.lock = Lock()
        # 登录验证
        self.listen_reader = Process(target=socket_service, args=(8888,))
        self.listen_admin = Process(target=socket_service, args=(8008,))
        # 执行操作
        self.execute = Process(target=socket_execute, args=(7777, self.lock,))

    def quit(self):
        self.listen_reader.terminate()
        self.listen_admin.terminate()
        self.execute.terminate()
        print("bye!")
        sys.exit(0)

    def run(self):
        print("欢迎使用杜文杰图书馆管理系统管理员服务器端1.0")
        print("input:'~e', 退出程序")
        print("input:'~p', 打印日志")
        print("强行退出会有残留子进程")
        # 启动子进程
        self.listen_reader.start()
        self.listen_admin.start()
        self.execute.start()
        while True:
            cin = input("input:")
            if cin == '~e':
                self.quit()
            elif cin == '~p':
                with open("logging_admin.txt", "r") as fp:
                    print(fp)
            else:
                print("错误的指令")


if __name__ == '__main__':
    Server().run()
