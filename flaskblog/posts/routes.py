from flask import Blueprint
from flask import render_template,url_for,flash,redirect,request,abort
from flask_login import current_user,login_required

from flaskblog.posts.forms import PostForm
from flaskblog.models import Post
from flaskblog import db



posts = Blueprint('posts',__name__)

@posts.route("/posts/new",methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # Creating a post with the data given in the form
        post = Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!",'success')
        return redirect(url_for("main.home"))
    return render_template("new_post.html",title="New Post",form=form,legend='New Post')


@posts.route("/posts/<int:post_id>")
def post(post_id):
    # Getting a post with its id
    post = Post.query.get_or_404(post_id)
    return render_template("post.html",title = post.title,post=post)

@posts.route("/posts/<int:post_id>/update",methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Checking if the current user is the author of the post
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated!",'success')
        return redirect(url_for("posts.post",post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    # Not creating an entirely new template for update_post
    # Just manipulating the existing template
    return render_template("new_post.html",title="Update Post",form=form,legend='Update Post')

@posts.route("/posts/<int:post_id>/delete",methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!",'success')
    return redirect(url_for('main.home'))