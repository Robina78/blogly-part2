"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool243243"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.route('/')
def root():
    """Show recent list of posts, most-recent first."""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("home.html", posts=posts)


@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404






@app.route('/')
def home():
    return redirect('/users')

@app.route('/users')
def user_list():
    users = User.query.all()
    return render_template('user_list.html', users=users)



@app.route('/users/new', methods=["GET"])
def users_form():
    return render_template('user_form.html')



@app.route('/users/new', methods=["POST"])
def create_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    
    db.session.add(new_user)
    db.session.commit()

    flash(f"User {new_user.full_name} added.", 'success')

    return redirect('/users')


@app.route('/users/<int:user_id>')  
def user_details(user_id):

    user = User.query.get_or_404(user_id)    
    return render_template('details.html', user=user)  


@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Show a form to edit an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} edited.", 'success')

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} deleted.", 'danger')
    return redirect("/users")

######################################### PART TWO ######################################################


@app.route('/users/<int:user_id>/posts/add')
def get_id_posts(user_id):

    user = User.query.get_or_404(user_id)
    return render_template('add_post.html', user=user)

@app.route('/users/<int:user_id>/posts/add', methods=["POST"])
def add_posts(user_id):

    user = User.query.get_or_404(user_id)
    title = request.form["title"]
    content = request.form["content"]
    new_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    flash(f"Post '{new_post.title}' added.", 'success')

    return redirect(f"/users/{user_id}")
  

@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    
    post = Post.query.get_or_404(post_id)
    return render_template('show.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def post_edit(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('edit_post.html', post=post)



@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):

    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.", 'success')

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["post"])
def del_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    flash(f"The {post.title} post is deleted.", 'danger')
    return redirect(f'/users/{post.user_id}')