import uuid
from common.db import Database
from models.blog import Blog
import datetime
from flask import session



class User(object):
    
    def __init__(self, email, password, _id = None):
        self.email = email 
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id
    
    @classmethod
    def get_by_email(cls, email):
        data  = Database.find_one("users", {"email": email})
        
        if data is not None:
            return cls(**data)
    
    @classmethod
    def get_by_id(cls,  _id):
        data  = Database.find_one("users", {"_id": _id})
        
        if data is not None:
            return cls(**data)
    
    @staticmethod
    def  login_valid(email, password):
        usrs  = User.get_by_email(email)
        
        if usrs is not None:
            return usrs.password == password 
        
        return False
    
    @classmethod
    def register(cls, email, password):
        usrs  = cls.get_by_email(email)
        
        if usrs is None:
            new_user = User(email, password)
            new_user.save_to_db()
            session['email'] = email
            return True
        else:
            return False
    
    @staticmethod
    def login(user_email):
        session['email'] = user_email
        
    @staticmethod
    def logout(user_email):
        session['email'] = None
    
    def get_blogs(self):
        return Blog.from_author_id(self._id)
    
    def json(self):
        return {
            'email' : self.email,
            '_id' : self._id,
            'password' : self.password 
        }
        
    def save_to_db(self):
        Database.insert("users", self.json())
        
        
    def new_blog(self, title, description):
        # title, description, author, author_id,
        
        blog = Blog(author = self.author,
                    title =  title,
                    description =  description,
                    author_id = self._id)
        
        blog.save_to_db()
        
    @staticmethod
    def new_post(blog_id, title, content, date = datetime.datetime.utcnow()):
        # title, description, author, author_id,
        
        blog = Blog.from_db(blog_id)
        
        blog.new_post(title = title,
                      content = content,
                      date = date)