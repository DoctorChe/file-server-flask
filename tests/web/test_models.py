import unittest

from project import create_app, db
from project.models import User, FileInfo


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user(self):
        u = User(name="user")
        self.assertEqual(u.name, "user")
        self.assertTrue(u.password_hash is None)
        self.assertEqual(u.files, [])

    def test_set_password(self):
        u = User(name="user")
        u.set_password("password")
        self.assertTrue(u.password_hash is not None)

    def test_check_password(self):
        u = User(name="user")
        u.set_password("password")
        self.assertTrue(u.check_password("password"))
        self.assertFalse(u.check_password("wrong_password"))


class FileInfoModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_file_info(self):
        file_info = FileInfo(name="file_name", user_id=1)
        self.assertEqual(file_info.name, "file_name")
        self.assertEqual(file_info.user_id, 1)
