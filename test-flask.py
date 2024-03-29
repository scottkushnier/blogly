

from models import db, User
from create_app import create_app
from unittest import TestCase
from dotenv import load_dotenv
from os import getenv

load_dotenv('.env.test')
app = create_app()

db.drop_all()
db.create_all()

class UsersTest(TestCase):
    def setUp(self):
        User.query.delete()
        user1 = User(first_name='Rocky', last_name='Squirrel')
        user2 = User(first_name='Bulwinkle',
                     last_name='Moose', image_url='images\moose.jpg')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        self.id1 = user1.id
        self.id2 = user2.id

    def tearDown(self):
        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get('/users/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Moose', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.id2}/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Moose', html)

    def test_show_new(self):
        with app.test_client() as client:
            resp = client.get('/users/new/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Create a User', html)

    def test_show_edit(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.id1}/edit/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Rocky', html)
