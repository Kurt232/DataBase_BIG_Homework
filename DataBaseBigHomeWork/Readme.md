# 数据库大作业

## 用python实现

### 表的设计
#### 读者表
"reader"
attributes: 
1. 读者号 "id_reader" int not null primary key auto_increment
2. 证件号 "certificate" int
3. 名字 "name" varchar(255) 
4. 性别 "sex" enum('male','female') not null 
5. 系号 "dept" varchar(255) 
6. 年级 "grade" int

#### 借还书表
"record"
attributes: 
1. 记录号 "id_record" int not null primary key auto_increment
2. 读者号 "id_reader" int not null foreign key 
3. 书籍号 "id_book" int not null foreign key 
4. 借书日期 "date_borrow" date
5. 应还书日期  "out_date" int


out_date(初始值为-1 正常还书为0 超期>0)
date 按照 yyyy-mm-dd 就是字符串


#### 书籍表
"book"
attributes: 
1. 书籍id "id_book" int not null primary key auto_increment
2. 书号 "book_no" int not null
3. 书名 "book_name" varchar(255) not null
4. 出版社 "publisher" varchar(255)
5. 出版日期 "date_publish" date
6. 作者 "author" varchar(255) 
7. 内容摘要 "abstract" varchar(255)


### 功能
- [x] 能够通过书籍基本信息（包括：书号、书名、出版社、出版日期、作者、内容摘要）单个或以AND方式组合多个条件查询书籍信息
- [x] 对于每一种书籍，除可查看其基本信息之外还可查看其总数以及目前在馆数量  
- [x] 可增添新的书籍  
- [x] 可删除已有书籍（如有读者借了该书籍尚未归还，则不允许删除）  
- [x] 可修改书籍的基本信息  
- [x] 能够通过读者基本信息（包括：证号、姓名、性别、系名、年级）单个或以AND方式组合多个条件查询读者信息  
- [x] 对于每位读者除可查看其基本信息之外，还可查看其已借的书籍列表、数量、借还日期  
- [x] 可增添新的读者  
- [x] 可删除已有读者（如该读者有尚未归还的借书，则不允许删除）  
- [x] 可修改读者的基本信息  
- [x] 可完成借还书籍的手续  
- [x] 还书时如超期，应该显示超期天数  
- [x] 借书时如果有超期的书没有还，则不允许借书  
- [x] 可查询有哪些读者有超期的书没有还，列出这些读者的基本信息  

### User类
- [x] 能够通过书籍基本信息（包括：书号、书名、出版社、出版日期、作者、内容摘要）单个或以AND方式组合多个条件查询书籍信息
- [x] 对于每一种书籍，除可查看其基本信息之外还可查看其总数以及目前在馆数量
### Administrator类
- [x] 可增添新的书籍  
- [x] 可删除已有书籍（如有读者借了该书籍尚未归还，则不允许删除）  
- [x] 可修改书籍的基本信息  
- [x] 能够通过读者基本信息（包括：证号、姓名、性别、系名、年级）单个或以AND方式组合多个条件查询读者信息  
- [x] 对于每位读者除可查看其基本信息之外，还可查看其已借的书籍列表、数量、借还日期  
- [x] 可增添新的读者  
- [x] 可删除已有读者（如该读者有尚未归还的借书，则不允许删除）
- [x] 可查询有哪些读者有超期的书没有还，列出这些读者的基本信息
- [x] 可修改读者的基本信息
### Reader类
- [x] 可完成借还书籍的手续  
- [x] 还书时如超期，应该显示超期天数  
- [x] 借书时如果有超期的书没有还，则不允许借书  
- [x] 对于每位读者除可查看其基本信息之外，还可查看其已借的书籍列表、数量、借还日期  
