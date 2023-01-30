import mysql.connector
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "bookstore"
)
mydb_Create_Table_Query = """CREATE TABLE usertype (
  id int(100) not null auto_increment,
  type varchar(50) not null,
CONSTRAINT type_pk PRIMARY KEY (id)
)"""
mydb_Create_Table_Query = """CREATE TABLE register
( id int(100) not null AUTO_INCREMENT PRIMARY KEY,
  fullname varchar(50) not null,
  username varchar(50) not null,
  password varchar(50) not null,
  type int(100) not null,
  FOREIGN KEY(type) REFERENCES usertype(id) 
)"""
# TABLE FOR STORING CATEGORY DETAILS OF BOOK
mydb_Create_Table_Query = """CREATE TABLE category
(categoryid int(100) not null auto_increment,
category varchar(50) not null,
CONSTRAINT category_pk PRIMARY KEY (categoryid)
)"""
# TABLE FOR STORING DETAILS OF BOOKS
mydb_Create_Table_Query = """CREATE TABLE book
(bookname varchar(50) not null,
isbn bigint(13) not null AUTO_INCREMENT PRIMARY KEY,
author varchar(50) not null,
category int(100) not null,
price numeric(50) not null,
FOREIGN KEY (category) REFERENCES category(categoryid)
)"""
cursor = mydb.cursor()
result = cursor.execute(mydb_Create_Table_Query)
print(" Table created successfully")
