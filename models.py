"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User Model"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String, nullable=True, default="https://i.stack.imgur.com/dr5qp.jpg")

    post = db.relationship('Post', backref="users", cascade="all, delete-orphan")

    #userposttags?

    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>"


class Post(db.Model):
    """Post model"""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    assignments = db.relationship('PostTag', backref='posts', cascade="all, delete-orphan")
    #check this delte later, it's so that tags won't get caught

    get_tags = db.relationship('Tag', secondary = 'posttags', backref='posts')

    def __repr__(self):
        p = self
        return f"<Post id={p.id} title={p.title} created_at={p.created_at} user={p.user_id}"

class Tag(db.Model):
    """Tag Model"""
    __tablename__ = 'tags'

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    assignments = db.relationship('PostTag', backref='tags', cascade="all, delete-orphan")
    #check this cascade latert

    get_posts = db.relationship('Post', secondary = 'posttags', backref='tags')

    def __repr__(self):
        return f"<Tag {self.name} id = {self.id}"

class PostTag(db.Model):
    """PostTag Model"""
    __tablename__ = 'posttags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True, nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True, nullable=False)
    #still unsure about making composite key
   

