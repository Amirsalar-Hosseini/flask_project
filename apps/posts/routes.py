from flask import Blueprint, render_template, redirect, flash, url_for, abort, request
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


@blueprint.route('/posts/detail/<int:post_id>', methods=['GET',])
def detail_post(post_id):
    post = db.session.execute(db.select(Post).where(Post.id==post_id)).scalar()
    if not post:
        flash('this post does not exist!', 'danger')
        if current_user.is_authenticated:
            return redirect(url_for('users.profile'))
        return redirect(url_for('home.home'))
    return render_template('posts/detail-post.html', post=post)


@blueprint.route('/posts/delete/<int:post_id>', methods=['GET',])
@login_required
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('users.profile'))


@blueprint.route('/posts/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    form = CreatePostForm()
    post = db.get_or_404(Post, post_id)
    if post.author != current_user:
        abort(403)
    if request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body
    elif request.method == 'POST':
        if form.validate_on_submit():
            post.title = form.title.data
            post.body = form.body.data
            db.session.commit()
            flash('Your post has been updated!', 'success')
            return redirect(url_for('posts.detail_post', post_id=post.id))

    return render_template('posts/update-post.html', form=form)