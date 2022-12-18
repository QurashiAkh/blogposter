from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialising the Flask App

app = Flask(__name__)

# Initialising the Database

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

# Creating a Model for posts


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, default='N/A')
    content = db.Column(db.Text, nullable=False, default='N/A')
    author = db.Column(db.String(30), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now())

# Routing


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts', methods=['GET', 'POST'])
@app.route('/posts/', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_author = request.form['author']
        post_content = request.form['content']

        new_post = Post(
            title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()

        return redirect('/posts/')

    else:
        all_posts = Post.query.order_by(Post.date_posted).all()
        return render_template('posts.html', posts=all_posts)

@app.route('/posts/new/')
@app.route('/posts/new')
def new_post():
    return render_template('new-post.html')

@app.route('/posts/<int:id>')
@app.route('/posts/<int:id>/')
def post(id):
    post = Post.query.get_or_404(id)
    
    return render_template('post.html', post=post)

@app.route('/posts/<int:id>/edit', methods=['GET', 'POST'])
@app.route('/posts/<int:id>/edit/', methods=['GET', 'POST'])
def edit(id):

    post = Post.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()

        return redirect('/posts/')

    else:
        return render_template('edit-post.html', post=post)

@app.route('/posts/<int:id>/delete')
@app.route('/posts/<int:id>/delete/')
def delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()

    return redirect('/posts/')

@app.route('/about')
@app.route('/about/')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=False)
