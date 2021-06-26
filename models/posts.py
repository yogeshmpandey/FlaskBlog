from pymongo import collection
import uuid
import datetime
from common.db import Database

class Post(object):
    
    def __init__(self, blog_id, title, content, author, created_date = datetime.datetime.utcnow(), _id = None):
        self.blog_id = blog_id
        self.content = content
        self.author = author
        self.created_date = created_date
        self._id = uuid.uuid4().hex if _id is None else _id
        self.title = title

    def save_to_db(self):
        Database.insert(collection='posts', data=self.convert_to_json())
    
    def convert_to_json(self):
        return { 
                '_id': self._id,
                'blog_id': self.blog_id,
                'author' : self.author,
                'content': self.content,
                'title': self.title,
                'created_date': self.created_date
                }
        
    @classmethod
    def from_db(cls, _id):
        data_val =  Database.find_one(collection='posts', query = {'_id':_id})
        
        return cls(**data_val)
        
        
    @staticmethod
    def from_blog(_id):
        return [post for post in Database.find(collection='posts', query = {'blog_id':_id})]
        