#flask login is a module used in flask web application to handle or manage the session of users
#first creating the usermodel to store the email and username and password to the database through
#orm object relationship mapper is a database engine or it is abstraction layer of database

#importing all the module used in web application

from flask_sqlalchemy import SQLAlchemy #THIS IS EXTERNAL ORM USED TO STORED DATA IN DATABASE

#creating an object of SQLAlchemy class
db = SQLAlchemy()

#importing the login manager class of flask login module to manage the session for every user
from flask_login import UserMixin,LoginManager #LoginManager will manage authenticate session for user...
#note:- usermixin will check the user is authenticated or not,active or not ,ananymous or not
#to check if login credentials provide is correct or not 

#creating an object of login manger class of flask login module
login = LoginManager()

#the password provided by the user wan tto store in database by applying hashing in it
#so we r using werkzeug module ka security outer class in which we r importing inner class check password or generate password hash
from werkzeug.security import generate_password_hash, check_password_hash


#now creating a table for usermodel to store details in database such as email and username and password

#so creating the class for usermodel

class UserModel(UserMixin,db.Model):
    #now using meta data for table name used by browser to give name of table in database
    __tablename__  = 'users'
    #now creating table in databse how many column present in table dtype of column and constraints of column
    id = db.Column('id',db.Integer,autoincrement=True,primary_key = True)
    username = db.Column('username',db.String(200),nullable=False)
    email = db.Column('email',db.String(200),nullable=False)
    password_hash = db.Column('password_hash',db.String(200),nullable=False)

    #want to store the password after hashing to the database mei
    #to achieve that we have to create a instance method to it

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    #if user doing login and feeding password in webpage se first we have to check the password is same or not
    #checking the password hashed value with original password

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)


    

#The user_loader callback in Flask is a function 
#that is used to load the user object for the current session
@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))

