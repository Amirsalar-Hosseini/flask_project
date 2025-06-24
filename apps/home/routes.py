from flask import Blueprint, render_template
from apps.extensions import db
from apps.posts.models import Post

blueprint = Blueprint('home', __name__)

@blueprint.route('/')
def home():
    posts = db.session.execute(db.select(Post).order_by(Post.created_at)).scalars()
    return render_template('home/home.html', posts=posts)