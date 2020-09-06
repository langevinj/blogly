"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, tzinfo, timezone, timedelta

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.Text,
                           nullable=False)
    
    last_name = db.Column(db.Text,
                          nullable=False)

    image_url = db.Column(db.String,
                          nullable=True,
                          default="https://i.stack.imgur.com/dr5qp.jpg")
    
    post = db.relationship('Post', cascade='all, delete')

    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>"

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.Text,
                      nullable=False)

    content = db.Column(db.Text,
                        nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'), db.relationship("User", cascade="all, delete-orphan"))

    user_id = db.Column(db.ForeignKey('users.id'))

    user = db.relationship('User')


    
    # def __init__(self, title, content):
    #     self.id = self.id
    #     self.title = title
    #     self.content = content
    #     self.created_at = datetime.now()

    # datetime.datetime(2020, 9, 6, 8, 12, 52, 396813)

    def __repr__(self):
        p = self
        return f"<Post id={p.id} title={p.title} created_at={p.created_at} user={p.user_id}"
   
    
