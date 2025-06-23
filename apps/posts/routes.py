from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import login_required, current_user
from apps.posts.forms import CreatePostForm
from apps.extensions import db
from apps.posts.models import Post

blueprint = Blueprint('posts', __name__)


@blueprint.route('/posts/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('users.profile'))
    return render_template('posts/create-post.html', form=form)