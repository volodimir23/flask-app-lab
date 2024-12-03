import json
import os

from . import posts_bp
from flask import render_template, abort, flash, redirect, url_for, session
from .forms import PostForm

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
    posts = load_posts(posts_file)
    return render_template('posts.html', posts=posts)

@posts_bp.route('/<int:id>')
def get_post(id):
    posts = load_posts(posts_file)
    if id < 1 or id > len(posts):
        abort(404)
    post = posts[id-1]
    return render_template('detail_post.html', post=post)

@posts_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        posts = load_posts(posts_file)
        author = session.get('username', 'Unknown')
        new_post = {
            "id": len(posts) + 1,
            "title": form.title.data,
            "content": form.content.data,
            "category": form.category.data,
            "is_active": form.is_active.data,
            "publication_date": form.publish_date.data.strftime("%Y-%m-%d"),
            "author": author
        }
        save_post(new_post)

        flash('Post added successfully!', 'success')
        return redirect(url_for('.get_posts'))
    return render_template('add_post.html', form=form)
