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
    def __init__(self,categoryid,category):
        self.categoryid=categoryid
        self.category=category
# CREATING CONSTRUCTOR FOR BOOK
class Book:
    def __init__(self,bookname, author, category, price):
        self.bookname=bookname
        self.author=author
        self.price=price
        self.category=category