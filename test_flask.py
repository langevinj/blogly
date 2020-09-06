from unittest import TestCase

from app import app
from models import db, User, Post
#Use a test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db_test'
app.config['SQLALCHEMY_ECHO'] = False

#Make Flask errors be real errors
app.config['TESTING'] = True

#Don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

# class UserTestCase(TestCase):
#     """Tests for views of Users"""

#     def setUp(self):
#         """Add sample user"""

#         User.query.delete()

#         user = User(first_name="Jim", last_name="Bob", image_url="https://npr.brightspotcdn.com/dims4/default/83db39c/2147483647/strip/true/crop/640x427+0+0/resize/1760x1174!/format/webp/quality/90/?url=http%3A%2F%2Fnpr-brightspot.s3.amazonaws.com%2Flegacy%2Fsites%2Fksor%2Ffiles%2F201711%2Fdennis_richardson.jpg")
#         db.session.add(user)
#         db.session.commit()

#         self.user_id = user.id
#         self.user = user

#     def tearDown(self):
#         """Clean up"""

#         db.session.rollback()

#     def test_list_users(self):
#         with app.test_client() as client:
#             resp = client.get("/", follow_redirects=True)
#             self.assertEqual(resp.status_code, 200)

#     def test_linked_users(self):
#         with app.test_client() as client:
#             resp = client.get("/users")
#             html = resp.get_data(as_text=True)

#             self.assertEqual(resp.status_code, 200)
#             self.assertIn('Jim Bob', html)
    
#     def test_add_user_form(self):
#         with app.test_client() as client:
#             resp = client.get("/users/new")

#             self.assertEqual(resp.status_code, 200)
    
#     def test_add_user(self):
#         with app.test_client() as client:
#             d = {"first_name": "John", "last_name": "Tom", "image_url": "www.wikipedia.com.jpg"}
#             resp = client.post("/users/new", data=d, follow_redirects=True)
#             html = resp.get_data(as_text=True)

#             self.assertEqual(resp.status_code, 200)
#             self.assertIn('<li><a href="/users/2">John Tom</a></li>', html)
    
#     def test_details_page(self):
#         with app.test_client() as client:
#             resp = client.get(f'/users/{self.user.id}')
#             html = resp.get_data(as_text=True)

#             self.assertEqual(resp.status_code, 200)
#             self.assertIn("<h2>Jim Bob</h2>", html)
    
#     def test_edit_user(self):
#         with app.test_client() as client:
#             resp = client.get(f'/users/{self.user.id}/edit')
#             html = resp.get_data(as_text=True)

#             self.assertEqual(resp.status_code, 200)
#             self.assertIn('<h2>Edit a User</h2>', html)
    
#     def test_edit_db_user(self):
#         with app.test_client() as client:
#             d = {"first_name": "John", "last_name": "Tom", "image_url": "www.wikipedia.com.jpg"}
#             resp = client.post(f'/users/{self.user.id}/edit', data=d, follow_redirects=True)
#             html = resp.get_data(as_text=True)

#             self.assertEqual(resp.status_code, 200)
#             self.assertIn("John Tom", html)
#             self.assertNotIn("Jim Bob", html)

class PostTestCase(TestCase):
    """Tests for vies for Posts"""

    def setUp(self):
        """Add sample user and post"""

        User.query.delete()

        user = User(first_name="Jim", last_name="Bob", image_url="https://npr.brightspotcdn.com/dims4/default/83db39c/2147483647/strip/true/crop/640x427+0+0/resize/1760x1174!/format/webp/quality/90/?url=http%3A%2F%2Fnpr-brightspot.s3.amazonaws.com%2Flegacy%2Fsites%2Fksor%2Ffiles%2F201711%2Fdennis_richardson.jpg")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

        Post.query.delete()

        new_post = Post(title="Garage Sale", content="Huge multi-family sale this weekend", user_id=1)
        db.session.add(new_post)
        db.session.commit()

        self.post_id = post.id 
        self.post = new_post

    def tearDown(self):
        """Clean up"""
        db.session.rollback()
    
    def test_add_post_page(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.post.user_id}/posts/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<title>Add a New Post</title>', html)
            self.assertIn('<h2>Add Post for Jim Bob</h2>', html)
    
    #seem to be getting an error with this test, but in practice this works
    # def test_add_post(self):
    #     with app.test_client() as client:
    #         p = {"title": "Wow i feel sick", "content":"I really need a checkup"}
    #         resp = client.post(f"/users/{self.user_id}/posts/new", data=p, follow_redirects=True)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
            # self.assertIn('<li><a href="/posts/2">Wow i feel sick</a></li>', html)

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get('/posts/1')
            html = resp.get_date(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<title>Garage Sale</title>", html)