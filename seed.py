"""Seed file to make sample data for blogly_db"""

from models import User, db, datetime, Post
from app import app

#Create all tables
db.drop_all()
db.create_all()

#If a table isn't empty, empty it
User.query.delete()

#Add users
john = User(first_name="John", last_name="Smith", image_url="https://yt3.ggpht.com/-_fExgATRXLY/AAAAAAAAAAI/AAAAAAAAAAA/-fmo8LhN7Pg/s240-c-k-no-rj-c0xffffff/photo.jpg")
jane = User(first_name="Jane", last_name="Doe", image_url="https://img.lovepik.com/photo/50076/1264.jpg_wh860.jpg")

#Add new users to session
db.session.add(john)
db.session.add(jane)

#Commit
db.session.commit()

#Add posts
van = Post(title="Wanted: Van", content="Looking for a good price on a solid van", created_at=datetime.now(), user_id=1)
guitarist = Post(title="ISO: Guitarist for Alt Rock Band", content="Gigging ever weekend, call 867-9305", created_at=datetime.now(), user_id=1)
first = Post(title="First Post", content="just testing things out", created_at=datetime.now(), user_id=2)
bookclub = Post(title="Starting a Bookclub", content="Would you like to join an up and coming bookclub? Email me here:", created_at=datetime(2020, 7, 4, 5, 2, 16, 540000), user_id=2)

#Add new posts to session
db.session.add(van)
db.session.add(guitarist)
db.session.add(first)
db.session.add(bookclub)

#Commit
db.session.commit()
