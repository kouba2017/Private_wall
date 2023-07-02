from flask_app.config.mysqlconnection import connectToMySQL
import re

from flask import flash

EMAIL_REGEX= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #specifies the layout of the email

class User:
    def __init__(self,data):
        self.id=data['id']
        self.first_name=data['firstName']
        self.last_name=data['lastName']
        self.email = data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
    @classmethod
    def save(cls,data):
        query="INSERT INTO users ( firstName, lastName, email,password,created_at) VALUES ( %(first_name)s, %(last_name)s, %(email)s,%(password)s,NOW());"
        return connectToMySQL('private_wall').query_db(query,data)
    @classmethod
    def get_by_id(cls,data):
        query="SELECT * FROM users WHERE id=%(id)s;"
        results= connectToMySQL('private_wall').query_db(query,data) 
        if len (results) <1:
            return False
        return cls(results[0])
    @classmethod
    def get_all(cls):
        query="SELECT*FROM users"
        results=connectToMySQL('private_wall').query_db(query)
        all_users=[]
        for user in results:
            all_users.append(cls(user))
        return all_users
    @classmethod
    def get_one(cls,data):
        query='SELECT * from users where '
    @classmethod
    def get_by_email(cls,data):
        query='SELECT * from users WHERE email=%(email)s;'
        results= connectToMySQL('private_wall').query_db(query,data)
        if len(results)<1:
            return False
        return cls(results[0])
    @staticmethod
    def validation(user):
        is_valid=True
        query="SELECT*FROM users WHERE email=%(email)s"
        result=connectToMySQL('login_regist').query_db(query,user)
        if len(result)>0:
            flash("Email already used, try to log in")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email, check your syntax","register")
            is_valid=False
        if user['password']!=user['confirm_password']:
            flash("passwords must match","register")
            is_valid=False
        if len(user['first_name'])<2:
            flash("first name must be at least 2 characters, required*","register")
            is_valid=False
        if len(user['last_name'])<2:
            flash("last name must be at least 2 characters,required*","register")
            is_valid=False
        if len(user['password'])<7:
            flash("password must be at least 8 characters,required*","register")
            is_valid=False
        return is_valid
