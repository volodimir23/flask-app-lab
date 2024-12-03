from flask import Flask


def create_app(config_name='config'):
    app = Flask(__name__)
    app.config.from_object(config_name)

    with app.app_context():
        from . import views

        from app.users import user_bp
        from app.posts import posts_bp
        app.register_blueprint(posts_bp)
        app.register_blueprint(user_bp)

    return app
