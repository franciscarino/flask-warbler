"""User model tests."""

from app import app
import os
from unittest import TestCase
from models import db, User, Message, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"


db.create_all()


class MessageModelTestCase(TestCase):
    def setUp(self):
        """set up before every test case"""
        Message.query.delete()
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        m1 = Message(text="test1message")
        u1.messages.append(m1)
        m2 = Message(text="test2message")
        u2.messages.append(m2)

        db.session.commit()

        self.u1_id = u1.id
        self.u2_id = u2.id

        self.m1_id = m1.id
        self.m2_id = m2.user_id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()


    def test_message_model(self):
        """Testing message to user model"""
        u1 = User.query.get(self.u1_id)
        m1 = Message.query.get(self.m1_id)

        self.assertEqual(len(u1.messages), 1)
        self.assertEqual(m1.text, "test1message")


    def test_message_not_in_user(self):
        """Testing user1 message not in user2"""

        u1 = User.query.get(self.u1_id)
        m2 = Message.query.get(self.m2_id)

        self.assertNotEqual(u1.messages, m2)
