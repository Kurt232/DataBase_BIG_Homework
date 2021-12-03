# -*- coding: utf-8 -*-
"""
---------------------------------------------------------
    File Name :         administrator                             
    Description :                                       
    Author :            Karl                             
    Date :              2021-12-01                          
---------------------------------------------------------
    Change Activity :   2021-12-01
    
--------------------------------------------------------- 
"""

# 定义Administrator的行为 进行封装
# 可以有多个管理员 同时在线
# 三个成员 管理员姓名 账号 密码
from user import *
from database_module import *


class Administrator(User):
    def __init__(self, name, account, db, cursor):
        super().__init__(account, db, cursor)
        self.name = name

    """add"""
    # pass test
    # 规定添加书籍各项数据都要正确 为空的话不予添加
    # book_no book_name publisher date_publish author abstract
    def add_book(self, info):
        info1 = []
        # 类型检查 没有检查 publish_date 的 date类型
        for i in info:
            if isinstance(i, str):
                info1.append("'" + i + "'")
            else:
                info1.append(str(i))
        insert_book(info1, self.db, self.cursor)

    # pass test
    # 规定增加读者各项数据都要正确
    # certificate name sex dept grad
    def add_reader(self, info):
        info1 = []
        # str类型检查
        for i in info:
            if isinstance(i, str):
                info1.append("'" + i + "'")
            else:
                info1.append(str(i))
        insert_reader(info1, self.db, self.cursor)

    """delete"""
    # info = id_book
    # 有书未还不能删除
    def delete_book(self, info) -> bool:
        flag = select_book_off(info, self.cursor)
        if not flag:
            return False
        delete_record(info, self.db, self.cursor)
        return True

    # info = id_reader
    # 有书未还不能删除
    def delete_reader(self, info) -> bool:
        flag = select_reader_is_borrow(info, self.cursor)
        if not flag:
            return False
        delete_reader(info, self.db, self.cursor)

    """update"""
    # 按照之前约定若是没有改变原有参数 以""表示
    # info = id_book
    def update_book(self, info):
        attribute = ["id_book", "book_no", "book_name", "publisher", "date_publish", "author", "abstract"]
        ls = select_update_all_id("book", info, self.cursor)
        info1 = [ls[0]]
        for i in range(1, len(ls)):
            if info[i] == "":
                info1.append(ls[i])
            else:
                if isinstance(str, info[i]):
                    info1.append("'" + info[i] + "'")
                else:
                    info1.append(str(info[i]))
        update_book(attribute, info1, self.db, self.cursor)

    # 按照之前约定若是没有改变原有参数 以""表示
    # info = id_reader
    def update_reader(self, info):
        attribute = ["id_reader", "certificate", "name", "sex", "dept", "grade"]
        ls = select_update_all_id("reader", info, self.cursor)
        info1 = [ls[0]]
        for i in range(1, len(ls)):
            if info[i] == "":
                info1.append(ls[i])
            else:
                if isinstance(str, info[i]):
                    info1.append("'" + info[i] + "'")
                else:
                    info1.append(str(info[i]))
        update_reader(attribute, info1, self.db, self.cursor)

    """ 查看读者界面"""
    # 组合查询读者
    # 返回值有 id_reader
    # 按照之前约定若是没有改变原有参数 以""表示
    # info 不包括 id_reader
    def query_reader(self, info) -> list:
        attribute = ["id_reader", "certificate", "name", "sex", "dept", "grade"]
        info1 = []
        for i in range(0, 5):
            if info[i] != "":
                info1.append(attribute[i+1])
                if isinstance(info[i], str):
                    info1.append("'" + info[i] + "'")
                else:
                    info1.append(str(info[i]))
        length = len(info1)
        return select_reader_all(info1, self.cursor)

    # 查看详细信息
    # 返回内容 [0]是id_reader
    # info = id_reader
    # -*- 这个框下方就是 修改同学信息按钮 -*-
    def view_reader_info(self, info) -> list:
        return select_reader(info, self.cursor)

    # 查看借还书情况
    # 未还书的记录再上面，上级界面检测到 out_date为-1即不显示即可
    # info = id_reader
    def view_reader_record(self, info) -> list:
        return select_record(info, self.cursor)

    """查询哪些读者没有及时还书界面"""
    # interval 是借书期限 也是全局变量
    def query_out_date(self, interval) -> list:
        return select_out_date(interval, self.cursor)
