# -*- coding: utf-8 -*-
"""
---------------------------------------------------------
    File Name :         client_admin                             
    Description :                                       
    Author :            Karl                             
    Date :              2021-12-09                          
---------------------------------------------------------
    Change Activity :   2021-12-09
    
--------------------------------------------------------- 
"""
import re
import sys

from mysocket import *
# 管理员 命令行实现


class Admin:
    def __init__(self):
        self.name = ""
        self.account = ""
        self.password = ""
        self.port = 4000
        self.online = False

    @staticmethod
    def help() -> str:
        return "'~e' 退出程序\n" \
               "'~r' 注册账号\n" \
               "'~l' 登录账号\n" \
               "'~o' 显示超期未还书籍的读者\n" \
               "以下为组合命令，若没有某信息，用','隔开\n" \
               "比如查看全体书籍:'~a ~b ;;;;;;'or'~a ~b'\n" \
               "比如通过书号查询书籍:'~a ~b 201031230;\n" \
               "比如通过出版社查询书籍:'~a ~b ;四川大学出版社;\n" \
               "一定不要在参数中乱加空格,不然查询不到\n" \
               "'~a ~b [书号;书名;出版社;出版日期;作者;内容摘要;]' 添加书籍\n" \
               "'~a ~r [证件号;姓名;性别;系号;年级;]' 添加读者\n" \
               "'~q ~b [书籍id;书号;书名;出版社;出版日期;作者;内容摘要;]' 查询书籍\n" \
               "'~q ~r [读者id;证件号;姓名;性别;系号;年级;]' 查询读者\n" \
               "'~d ~b [书籍id;书号;书名;出版社;出版日期;作者;内容摘要;]' 删除书籍\n" \
               "'~d ~r [读者id;证件号;姓名;性别;系号;年级;]' 删除读者\n" \
               "'~c ~b [书籍id;书号;书名;出版社;出版日期;作者;内容摘要;]' 查询某本书籍的借书记录\n" \
               "'~c ~r [读者id;证件号;姓名;性别;系号;年级;]' 查询某位学生的借书记录\n" \
               "'~u ~b [书号;书名;出版社;出版日期;作者;内容摘要;] [书号;书名;出版社;出版日期;作者;内容摘要;]' 更新书籍信息\n" \
               "前面为原始信息,后面为修改过后信息\n" \
               "'~u ~r [证件号;姓名;性别;系号;年级;] [证件号;姓名;性别;系号;年级;]' 更新读者信息\n" \
               "前面为原始信息,后面为修改过后信息\n"

    @staticmethod
    def input():
        return input("input:")

    def login(self):
        while not self.online:
            print("请输入账号")
            self.account = self.input()
            if self.account == '~e':
                print("bye!")
                sys.exit(0)
            elif len(self.account) > 100000000:
                print("用户名太长")
                continue
            elif self.account[0] == '~':
                print("含有非法的字符")
                continue
            print("请输入密码")
            self.password = input()
            print("正在登录，请稍等")
            info = {"type": "login", "account": self.account, "password": self.password}
            data = json.dumps(info)
            check: str = socket_client(data, self.port)
            if check == "404":
                print("与服务器未连接")
            elif check == "failure":
                print("账号或密码错误")
            else:
                rec = json.loads(check)
                self.port = rec["port"]
                self.name = rec["name"]
                self.online = True
                print("登录成功, 欢迎管理员" + self.name + "!")

    def regedit(self,):
        while not self.online:
            print("请输入账号")
            self.account = self.input()
            if self.account == '~e':
                sys.exit(0)
            elif len(self.account) > 100000000:
                print("用户名太长")
                continue
            elif self.account[0] == '~':
                print("含有非法的字符")
                continue
            print("请输入账号")
            self.account = self.input()
            if self.account == '~e':
                sys.exit(0)
            elif len(self.account) > 100000000:
                print("用户名太长")
                continue
            elif self.account[0] == '~':
                print("含有非法的字符")
                continue
            print("请输入密码")
            self.password = self.input()
            print("请输入用户名")
            self.name = self.input()
            print("正在注册，请稍等")
            info = {"type": "regedit", "name": self.name, "account": self.account, "password": self.password}
            data = json.dumps(info)
            check: str = socket_client(data, self.port)
            if check == "404":
                print("与服务器未连接")
            else:
                rec = json.loads(check)
                self.port = rec["port"]
                self.name = rec["name"]
                self.online = True
                print("注册成功, 欢迎管理员" + self.name + "!")

    @staticmethod
    def update_info(typee, info, lenn, length) -> dict:
        data = {"type": typee, "info": []}
        for i in range(2, length):
            data["info"].append(info[i])
        for i in range(length, lenn):
            data["info"].append("")
        return data

    def sendall(self, data, title):
        msg = json.dumps(data)
        fd = socket_client(msg, self.port)
        if fd == "404":
            self.online = False
            return "登录过期"
        else:
            info = json.loads(fd)
            print(title)
            for i in info:
                for j in i:
                    print(j, end=" ")
                print("-------------------------------------------------")
            return "执行完毕"

    def deal(self, cin) -> str:
        # 其实应该针对每一个选择情况写一个正则表达式
        re0 = re.compile(r'(~[oelrh])$')
        re1 = re.compile(r'^(~[adqc]) (~[br]) (.*;){0,7}$')
        re2 = re.compile(r"^(~[u]) (~[br]) ((.*;){1,6}) ((.*;){1,6})$")
        data = {"type": "", "info": []}
        if re0.match(cin):
            info = re0.findall(cin)
            if info[0] == '~e':
                print("bye!")
                sys.exit(0)
            elif info[0] == '~l':
                if not self.online:
                    self.login()
                    return "执行完毕"
                else:
                    return "您已登录"
            elif info[0] == '~r':
                return "您已登录"
            elif info[0] == '~h':
                return self.help()
            elif info[0] == '~o':
                data["type"] = "query_out_date"
                return self.sendall(data, "超期读者信息")
        elif re1.match(cin):
            info = re1.findall(cin)
            length = len(info)
            if info[0] == '~a':
                if info[1] == '~b':
                    if length > 8:
                        return "语法错误, 参数过多"
                    data = self.update_info("add_book", info, 8, length)
                    return self.sendall(data, "添加书籍")
                elif info[1] == '~r':
                    if length > 7:
                        return "语法错误, 参数过多"
                    data = self.update_info("add_reader", info, 7, length)
                    return self.sendall(data, "添加读者")
            elif info[0] == '~d':
                if info[1] == '~b':
                    data = self.update_info("delete_book", info, 9, length)
                    return self.sendall(data, "删除书籍")
                elif info[1] == '~r':
                    if length > 8:
                        return "语法错误, 参数过多"
                    data = self.update_info("delete_reader", info, 8, length)
                    return self.sendall(data, "删除读者")
            elif info[0] == '~q':
                if info[1] == '~b':
                    if length > 9:
                        return "语法错误, 参数过多"
                    data = self.update_info("query_book", info, 9, length)
                    return self.sendall(data, "查询书籍")
                elif info[1] == '~r':
                    if length > 8:
                        return "语法错误, 参数过多"
                    data = self.update_info("query_reader", info, 8, length)
                    return self.sendall(data, "查询读者")
            elif info[0] == '~c':
                if info[1] == '~b':
                    if length > 9:
                        return "语法错误, 参数过多"
                    data = self.update_info("record_book", info, 9, length)
                    return self.sendall(data, "查询书籍记录")
                elif info[1] == '~r':
                    if length > 8:
                        return "语法错误, 参数过多"
                    data = self.update_info("record_reader", info, 8, length)
                    return self.sendall(data, "查询读者记录")
        elif re2.match(cin):
            info = re2.findall(cin)
            length1 = len(info[2])
            length2 = len(info[3])
            if info[0] == '~u':
                if info[1] == '~b':
                    data = {"type": "record_book", "info": [[], []]}
                    for i in info[2]:
                        data["info"][0].append(i)
                    for i in range(length1, 7):
                        data["info"][0].append("")
                    for i in info[3]:
                        data["info"][1].append(i)
                    for i in range(length2, 7):
                        data["info"][1].append("")
                    return self.sendall(data, "查询书籍记录")
                elif info[1] == '~r':
                    data = {"type": "record_reader", "info": [[], []]}
                    for i in info[2]:
                        data["info"][0].append(i)
                    for i in range(length1, 7):
                        data["info"][0].append("")
                    for i in info[3]:
                        data["info"][1].append(i)
                    for i in range(length2, 7):
                        data["info"][1].append("")
                    return self.sendall(data, "查询读者记录")
        else:
            return "语法有误"

    def run(self):
        print("****************************************")
        print("*欢迎使用杜文杰图书馆管理系统——管理员端1.0   *")
        print("*输入'~e',退出系统                       *")
        print("*输入'~h',帮助菜单                       *")
        print("*输入'~l',进行登录                       *")
        print("*输入'~r',注册账号                       *")
        print("****************************************")
        cin = self.input()
        flag = True
        while flag:
            if cin == '~e':
                print("bye!")
                sys.exit(0)
            elif cin == '~l':
                flag = False
                self.login()
            elif cin == '~r':
                flag = False
                self.regedit()
            elif cin == '~h':
                print(self.help())
                cin = self.input()
            else:
                print("错误的指令")
                cin = self.input()
        while True:
            cin = self.input()
            print(self.deal(cin))


if __name__ == '__main__':
    Admin().run()
