"""Seed file to make sample data for blogly_db"""

from models import User, db
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