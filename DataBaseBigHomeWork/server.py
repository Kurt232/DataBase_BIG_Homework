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
import json
import multiprocessing.synchronize
import sys
from multiprocessing.synchronize import Lock

from administrator import *
from database_module import *
from mysocket import *
from multiprocessing import Process, Lock


class Server:

    def __init__(self,):
        with open("regedit.json", "r") as fp:
            regedit = json.load(fp)
            self.db, self.cursor = connect_database(regedit["login"])
            fp.close()
        self.admin = Administrator("root", "root", self.db, self.cursor)
        self.lock = Lock()
        # 登录验证
        self.listen_reader = Process(target=socket_service, args=(8888,))
        self.listen_admin = Process(target=socket_service, args=(8000,))
        # 执行操作
        self.execute = Process(target=socket_execute, args=(False, 7777, self.db, self.cursor, self.lock))
        # 启动子进程
        self.listen_reader.start()
        self.listen_admin.start()
        self.execute.start()

    def quit(self):
        self.listen_reader.close()
        self.listen_admin.close()
        self.execute.close()
        print("bye!")
        sys.exit(0)

    def run(self):
        print("欢迎使用杜文杰图书馆管理系统管理员服务器端1.0")
        print("input:'~e', 退出程序")
        print("input:'~p', 打印日志")
        print("强行退出会有残留子进程")
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
    Server.run()
