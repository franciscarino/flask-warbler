"""User views tests."""

import os
from unittest import TestCase
from models import db, User, Message, Like, DEFAULT_IMAGE_URL
from app import CURR_USER_KEY, app

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

app.config['WTF_CSRF_ENABLED'] = False

db.create_all()

class UserViewsTestCase(TestCase):
    def setUp(self):
        """set up for every test"""

        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.add_all([u1, u2])
        db.session.commit()

        self.u1_id = u1.id
        self.u2_id = u2.id

        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        u1.following.append(u2)

        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()


    def test_post_signup(self):
        """Testing signup"""
        with self.client as c:
            post_resp = c.post("/signup", data={"username": "u10",
                                            "password": "password",
                                            "email": "u10@email.com",
                                            "image_url": DEFAULT_IMAGE_URL},
                                            follow_redirects=True)

            html = post_resp.get_data(as_text=True)

            self.assertEqual(post_resp.status_code, 200)
            self.assertIn('THIS IS THE HOMEPAGE', html)
            self.assertIn("u10", html)

    def test_get_signup(self):
        """Testing signup"""
        with self.client as c:
            resp = c.get("/signup")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('THIS IS THE SIGNUP PAGE', html)

    def test_get_user_login(self):
        """Testing user login get request"""
        with self.client as c:
            resp = c.get("/login")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('THIS IS THE LOGIN PAGE', html)

    def test_post_user_login(self):
        """Testing user login post request"""
        with self.client as c:
            resp = c.post("/login", data = {
                                    "username": "u1",
                                    "password": "password"
                                    },
                                    follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('THIS IS THE HOMEPAGE', html)

    def test_list_users(self):
        """Testing list of users"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            resp = c.get("/users")

            self.assertEqual(resp.status_code, 200)
            self.assertIn("@u1", str(resp.data))
            self.assertIn("@u2", str(resp.data))

    def test_show_user(self):
        """Testing user details"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            resp = c.get(f"/users/{self.u1_id}")
            bad_resp = c.get(f"/users/100")

            self.assertEqual(bad_resp.status_code, 404)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("@u1", str(resp.data))

    def test_user_following(self):
        """Testing user following"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            resp = c.get(f"/users/{self.u1_id}/following")
            not_following_resp = c.get(f"/users/{self.u2_id}/following")

            self.assertEqual(resp.status_code, 200)
            self.assertIn("@u2", str(resp.data))
            self.assertNotIn("@u1", str(not_following_resp.data))



