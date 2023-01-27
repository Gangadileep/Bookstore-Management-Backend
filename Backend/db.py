import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "bookstall"
)
mydb_Create_Table_Query = """CREATE TABLE register
( fullname varchar(50) not null,
  username varchar(50) not null,
  email varchar(50) not null,
  password varchar(50) not null
)"""
mydb_Create_Table_Query = """CREATE TABLE book
( bookname varchar(50) not null,
  isbn numeric(10) not null,
  author varchar(50) not null,
  category  varchar(50) not null,
  prize numeric(10) not null,
  CONSTRAINT book_pk PRIMARY KEY (isbn)
)"""
cursor = mydb.cursor()
result = cursor.execute(mydb_Create_Table_Query)
print(" Table created successfully ")
