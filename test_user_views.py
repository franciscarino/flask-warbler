"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Like, DEFAULT_IMAGE_URL

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import CURR_USER_KEY, app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

class UserViewsTestCase(TestCase):
    def setUp(self):
        """set up for every test"""

        Message.query.delete()
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        m1 = Message(text="test1message")
        u1.messages.append(m1)
        m2 = Message(text="test2message")
        u2.messages.append(m2)


        l1 = Like(user_like_id =u1, message_id=m2)
        l2 = Like(user_like_id =u2, message_id=m1)

        db.session.commit()

        self.u1_id = u1.id
        self.u2_id = u2.id

        self.m1_id = m1.id
        self.m2_id = m2.user_id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()


    def test_post_signup(self):
        """Testing signup"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u10
            post_resp = c.post("/signup", data={"username": "u10",
                                            "password": "password",
                                            "email": "u10@email.com",
                                            "image_url": DEFAULT_IMAGE_URL},
                                            follow_redirects=True)
            # get_resp = c.get("/signup")
            html = post_resp.get_data(as_text=True)

            breakpoint()

            self.assertEqual(post_resp.status_code, 200)
            self.assertIn('THIS IS THE HOMEPAGE', html)
            self.assertIn("u3", html)

    def test_get_signup(self):
        """Testing signup"""
        with self.client as c:
            resp = c.get("/signup")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('THIS IS THE SIGNUP PAGE', html)

