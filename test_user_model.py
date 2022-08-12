"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
        """set up for every test"""
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        """Testing user model"""
        u1 = User.query.get(self.u1_id)

        # User should have no messages & no followers
        self.assertEqual(len(u1.messages), 0)
        self.assertEqual(len(u1.followers), 0)

    def test_user_repr(self):
        """Testing user repr"""

        u1 = User.query.get(self.u1_id)

        self.assertIn("<User #", repr(u1))

    def test_following(self):
        """Testing following functions"""

        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        u1.following.append(u2)
        db.session.commit()

        self.assertEqual([u2], u1.following)
        self.assertEqual([u1], u2.followers)

    def test_not_following(self):
        """Testing that users are not following """

        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        self.assertNotEqual([u2], u1.following)
        self.assertNotEqual([u1], u2.followers)

    def test_user_signup(self):
        """Testing user signup"""

        u3 = User.signup("u3", "u3@email.com", "password", None)

        db.session.add(u3)
        db.session.commit()

        users = User.query.all()

        self.assertIn(u3, users)

    # def test_fail_user_signup(self):
    #     """Testing failed user signup with failed validation"""

    #     u3 = User.signup("u1", "u1@email.com", None, None)

    #     db.session.add(u3)
    #     db.session.commit()

    #     # users = User.query.all()

    #     self.assertRaises(ValueError, User.signup("u1", "u1@email.com", None, None))

    def test_user_authentication(self):
        """Testing authenticating user successfully"""

        u1 = User.query.get(self.u1_id)

        user = User.authenticate(
            "u1",
            "password")

        self.assertEqual(u1, user)

    def test_fail_user_authentication(self):
        """Testing failed authentication"""

        user = User.authenticate(
            "u3",
            "password")

        user2 = User.authenticate(
            "u2",
            "wrongpassword")

        self.assertEqual(False, user)
        self.assertEqual(False, user2)



