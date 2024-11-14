from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('../config.py')


from . import views
from app.users import user_bp
from app.posts import posts_bp

app.register_blueprint(posts_bp)
app.register_blueprint(user_bp)
