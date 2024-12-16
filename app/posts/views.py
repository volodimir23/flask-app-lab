import json
import os

from . import posts_bp
from flask import render_template, abort, flash, redirect, url_for, session
from .forms import PostForm
from .models import Post
from app import db

# posts = [
#     {"id": 1, 'title': 'My First Post', 'content': 'This is the content of my first post.', 'author': 'John Doe'},
#     {"id": 2, 'title': 'Another Day', 'content': 'Today I learned about Flask macros.', 'author': 'Jane Smith'},
#     {"id": 3, 'title': 'Flask and Jinja2', 'content': 'Jinja2 is powerful for templating.', 'author': 'Mike Lee'}
# ]

posts_file = 'app/posts/posts.json'

def load_posts(file):
    if not os.path.exists(file):
        return []
    with open(file, 'r') as f:
        data = json.load(f)
        return data

def save_post(post):
    posts = load_posts(posts_file)
    posts.append(post)
    with open(posts_file, 'w') as f:
        json.dump(posts, f, indent=4)

@posts_bp.route('/')
def get_posts():
    #posts = load_posts(posts_file)
    posts = Post.query.order_by(Post.posted.desc()).all()
    return render_template('posts.html', posts=posts)

@posts_bp.route('/<int:id>')
def get_post(id):
    # posts = load_posts(posts_file)
    # if id < 1 or id > len(posts):
    #     abort(404)
    # post = posts[id-1]
    post = Post.query.get_or_404(id)
    return render_template('detail_post.html', post=post)

@posts_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        posts = load_posts(posts_file)
        author = session.get('username', 'Unknown')
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            is_active=form.is_active.data,
            posted=form.publish_date.data,
            author=author
        )
        #save_post(new_post)
        db.session.add(new_post)
        db.session.commit()

        flash('Post added successfully!', 'success')
        return redirect(url_for('.get_posts'))
    return render_template('add_post.html', form=form)

@posts_bp.route('/remove_post/<int:id>')
def remove_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Post removed successfully!', 'success')
    return redirect(url_for('.get_posts'))

@posts_bp.route('/edit_post/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm(obj=post)
    form.publish_date.data = post.posted
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = form.is_active.data
        post.posted = form.publish_date.data
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('.get_posts'))
    return render_template('edit_post.html', form=form)
