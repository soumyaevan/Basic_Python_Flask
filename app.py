from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default="Unknown")
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return 'Bog post ' + str(self.id)


all_friends =[
    {'name':'Pranoy Das', 'age':27, 'address':'Birati', 'relationship':'In a relationship'},
    {'name':'Arup Biswas', 'age':26, 'address':'Titagarh'}
]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home')
def home():
    return "This is home page"

@app.route('/posts',methods=['GET','POST'])
def get_posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_Post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_Post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template("posts.html",posts=all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session().delete(post)
    db.session().commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template("edit.html", post=post)

@app.route('/posts/new',methods=['GET','POST'])
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_Post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_Post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template("new_post.html")

@app.route('/posts/blog/<string:text>',methods=['GET','POST'])
def get_Blog(text):
    author_text = BlogPost.query.filter_by(author=text).all()
    title_text = BlogPost.query.filter_by(title=text).all()
    if author_text:
        return render_template("blog.html",posts=author_text)
    elif title_text:
        return render_template("blog.html",posts=title_text)
    else:
        return redirect('/posts')

# Dynamic URL
@app.route('/user/<string:name>')
def print_name(name):
    return f"Hello {name}"

# Filtering request
@app.route('/getonly',methods=['GET'])
def get_req():
    return "This web page supports only get request 1"

@app.route('/friends')
def get_friends():
    return render_template("friends.html",friends=all_friends)

if __name__ == "__main__":
    app.run(debug=True)