from pymongo import collection
import uuid
import datetime
from common.db import Database
from models.posts import Post

class Blog(object):
    
    def __init__(self, title, description, author, author_id, _id = None):
        self.description = description
        self.author = author
        self._id = uuid.uuid4().hex if _id is None else _id
        self.title = title
        self.author_id = author_id


    def new_post(self, title, content, date= datetime.datetime.utcnow()):
        post = Post(_id = self.id, title = title, content= content, author= self.author, created_date = date)
        post.save_to_db()
        
    def save_to_db(self):
        Database.insert(collection='blogs', data=self.convert_to_json())
    
    def convert_to_json(self):
        return { 
                
                '_id': self._id,
                'author' : self.author,
                'author_id' : self.author_id,
                'description': self.description,
                'title': self.title
                }
        
    @classmethod
    def from_db(cls, _id):
        blog_data =  Database.find_one(collection='blogs', query = {'_id':_id})
        return cls(**blog_data)
        
        
    @classmethod
    def from_author_id(cls, author_id):
        blog_data =  Database.find(collection='blogs', query = {'author_id':author_id})
        
        # TODO
        return [cls(**blog) for blog in blog_data]
    
    @staticmethod
    def from_blog(_id):
        return [post for post in Database.find(collection='posts', query = {'_id':_id})]
    
    def get_posts(self):
        return Post.from_blog(self._id)
        