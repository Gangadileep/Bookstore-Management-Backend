# CREATING CONSTUCTOR 
class Usertype:
    def __init__(self,id,type):
        self.id=id
        self.type=type
# CREATING CONSTRUCTOR FOR REGISTER
class Register:
    def __init__(self,id,fullname,username,password,type):
        self.id=id
        self.fullname=fullname
        self.username=username
        self.password=password
        self.type=type
# CREATING CONSTRUCTOR
class Category:
    def __init__(self,id,category):
        self.id=id
        self.category=category
# CREATING CONSTRUCTOR FOR BOOK
class Book:
    def __init__(self,isbn,bookname, author, categoryid, price,adminid):
        self.isbn=isbn
        self.bookname=bookname
        self.author=author
        self.categoryid=categoryid
        self.price=price
        self.adminid=adminid