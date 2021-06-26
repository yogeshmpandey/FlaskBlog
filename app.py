from flask.helpers import make_response
from common.db import Database
from models.blog import Post
from models.users import User
from models.blog import Blog
from flask import Flask, render_template, request, session

app = Flask(__name__)

app.secret_key = "yogesh"


@app.route('/')
def hello_template():
    return render_template("login.html")

@app.route('/login')
def login_template():
    return render_template("login.html")


@app.route('/register')
def register_template():
    return render_template("register.html")

@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/auth/login', methods = ['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']
    
    if User.login_valid(email, password):
        User.login(email)
    else:
        session['email'] = None 
        return render_template("login.html")       
    return render_template("profile.html", email = session['email'])




@app.route('/auth/register', methods = ['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']
    
    User.register(email, password)
    return render_template("profile.html", email = session['email'])


@app.route('/blogs/<string:user_id>')
@app.route('/blogs/')
def user_blog(user_id = None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])
         
    blogs = user.get_blogs()
    return render_template("user_blogs.html", blogs=blogs, email = user.email)

@app.route('/posts/<string:blog_id>')
@app.route('/posts/')
def blog_posts(blog_id = None):

    blog = Blog.from_db(blog_id)
    posts = blog.get_posts()
    for post in posts:
        print ("{0}".format(post))
    return render_template("posts.html", posts=posts, blog_title = blog.title, blog_id = blog._id)


@app.route('/blogs/new', methods = ['POST', 'GET'])
def create_new_blog():
    if request.method == 'GET':
        return render_template('new_blog.html')
    
    else:
        title = request.form['title']
        description = request.form['description']
        user = User.get_by_email(session['email'])
        print(title)
        #title, description, author, author_id, _id = None
        new_blog = Blog(title, description, user.email, user._id)
        new_blog.save_to_db()

        # redurect to the above function
        return make_response(user_blog(user._id))


@app.route('/posts/new/<string:blog_id>', methods = ['POST', 'GET'])
def create_new_post(blog_id):
    if request.method == 'GET':
        return render_template('new_post.html', blog_id=blog_id)
    
    else:
        title = request.form['title']
        content = request.form['content']
        user = User.get_by_email(session['email'])
        print(title)
        #title, description, author, author_id, _id = None
        new_post = Post(blog_id, title, content, user.email)
        new_post.save_to_db()

        # redurect to the above function
        return make_response(blog_posts(blog_id))


if __name__ == '__main__':
    app.run()
