"""Blogly application."""

from flask import Flask, render_template, request, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, datetime, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secretcode123123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/")
def list_users():
    """Shows list of all users in the db"""

    return redirect('/users')

@app.route("/users")
def linked_users():
    """Show a list of users with links to their details, and a button to add a new user"""
    users = User.query.all()
    return render_template ('users.html', users=users)

@app.route("/users/new", methods=["GET"])
def add_user_form():
    """Form to add a new user"""
    return render_template ('add_user.html')

@app.route("/users/new", methods=["POST"])
def add_user():
    """Adds user to db"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    image_url = image_url if image_url else None

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect ('/users')

@app.route('/users/<int:userid>')
def details_page(userid):
    """Shows specified user's details page"""
    user = User.query.get_or_404(userid)
    posts = Post.query.filter(Post.user_id == userid).all()
    return render_template("details.html", user=user, posts=posts)

@app.route('/users/<int:userid>/edit')
def edit_user(userid):
    """Edit a specific user"""
    user = User.query.get_or_404(userid)
    return render_template("edit_user.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_db_user(user_id):
    """Update a user based on edits"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    
    return redirect("/users")

@app.route('/users/<int:userid>/delete', methods=["POST"])
def delete_user(userid):
    """Delete a specific user"""
    user = User.query.get(userid)
    db.session.delete(user)
    db.session.commit()
    return redirect ("/users")


@app.route('/users/<int:userid>/posts/new')
def add_post_page(userid):
    """Page for adding a new post"""
    user = User.query.get(userid)
    tags= Tag.query.all()
    return render_template('add_post.html', user=user, tags=tags)


@app.route('/users/<int:userid>/posts/new', methods=["POST"])
def add_post(userid):
    """Add new post"""
    user = User.query.get(userid)
    tag_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form['title'], content=request.form['content'], user_id=user.id,  tags=tags)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user.id}')

@app.route('/posts/<int:postid>')
def show_post(postid):
    """Show a given post"""
    post = Post.query.get(postid)
    author = User.query.get(post.user_id)
    date = post.date_cleaner()
    return render_template('show_post.html', post=post, author=author, date=date)

@app.route('/posts/<int:postid>/edit')
def edit_post_page(postid):
    """Show page to edit a post"""
    post = Post.query.get(postid)
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post, tags=tags)


@app.route('/posts/<int:postid>/edit', methods=["POST"])
def edit_post(postid):
    """Show page to edit a post"""
    post = Post.query.get(postid)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:postid>/delete', methods=['POST'])
def delete_post(postid):
    """Delete a post"""
    post = Post.query.get(postid)

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')

@app.route('/tags')
def list_tags():
    """List all tags"""
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tagid>')
def tag_details(tagid):
    """Show tag details page"""
    tag = Tag.query.get(tagid)
    posts = tag.get_posts
    return render_template('tag_details.html', tag=tag, posts=posts)

@app.route('/tags/new')
def new_tag_form():
    """Page to add a new tag"""
    return render('add_tag.html')

@app.route('/tags/new', methods=['POST'])
def add_new_tag():
    """Adds a new tag"""
    new_tag = request.form["newtag"]
    tag = Tag(name=new_tag)

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tagid>/edit')
def show_edit_form(tagid):
    target = Tag.query.get(tagid)

    return render_template('edit_tag.html', tag=target)

@app.route('/tags/<int:tagid>/edit', methods=["POST"])
def edit_tag(tagid):
    """Edits a tag"""
    target = Tag.query.get(tagid)
    edittag = request.form['edittag']
    target.name = edittag

    db.session.add(target)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tagid>/delete', methods=["POST"])
def delete_tag(tagid):
    """Delete a tag"""
    target = Tag.query.delete(tagid)

    db.session.delete(target)
    db.session.commit()

    return redirect('/tags')
