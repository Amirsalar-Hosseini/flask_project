from flask import Flask
from apps.posts.routes import blueprint as posts_blueprint
from apps.users.routes import blueprint as users_blueprint
from apps.home.routes import blueprint as home_blueprint
from apps.extensions import db, hashing, login_manager
import apps.exceptions as app_exceptions


def register_blueprints(app):
    app.register_blueprint(posts_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(home_blueprint)

def register_error_handlers(app):
    app.register_error_handler(404, app_exceptions.page_not_found)
    app.register_error_handler(403, app_exceptions.permission_error)
    app.register_error_handler(500, app_exceptions.server_error)

app = Flask(__name__)
register_blueprints(app)
register_error_handlers(app)
app.config.from_object('config.DevelopmentConfig')


db.init_app(app)
from apps.users.models import User
from apps.posts.models import Post
with app.app_context(): db.create_all()

hashing.init_app(app)

login_manager.init_app(app)
login_manager.login_view = 'users.login'
login_manager.login_message = 'dont do that right now ;|'
login_manager.login_message_category = 'warning'