import unittest

from project import create_app, db


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_404(self):
        response = self.client.get("/wrong/url")
        self.assertEqual(response.status_code, 404)

    def test_no_auth(self):
        response = self.client.post("/files/")
        self.assertEqual(response.status_code, 401)
