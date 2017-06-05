import datetime
import unittest
import uuid
from nc_user import create_app
from nc_user.api.schema import *


class UserSchemaTestCase(unittest.TestCase):


    def setUp(self):
        self.app = create_app("test")
        self.app.config["TESTING"] = True
        self.app.config["SERVER_NAME"] = "localhost"

        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = self.app.test_client()
        self.schema = UserSchema()


    def tearDown(self):
        self.schema = None

        self.app_context.pop()


    def test_empty1(self):
        client_data = {
        }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
            "_schema": ["Input data must have a user key"]
        })


    def test_empty2(self):
        client_data = {
            "user": {}
        }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
            "id": ["Missing data for required field."],
            "e_mail": ["Missing data for required field."],
        })


    def test_invalid_user(self):
        client_data = {
            "user": {
                "id": "blah",
                "e_mail": "meh@mah.org",
            }
        }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
            "id": ["Not a valid UUID."],
        })


    def test_invalid_e_mail(self):
        client_data = {
            "user": {
                "id": uuid.uuid4(),
                "e_mail": "meh",
            }
        }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
            "e_mail": ["Not a valid email address."],
        })


    def test_usecase1(self):

        client_data = {
            "user": {
                "id": uuid.uuid4(),
                "e_mail": "meh@mah.org",
            }
        }
        data, errors = self.schema.load(client_data)

        self.assertFalse(errors)

        self.assertTrue(hasattr(data, "id"))
        self.assertTrue(isinstance(data.id, uuid.UUID))

        self.assertTrue(hasattr(data, "e_mail"))
        self.assertEqual(data.e_mail, "meh@mah.org")

        self.assertTrue(hasattr(data, "create_stamp"))
        self.assertTrue(isinstance(data.create_stamp, datetime.datetime))

        self.assertTrue(hasattr(data, "edit_stamp"))
        self.assertTrue(isinstance(data.edit_stamp, datetime.datetime))

        data.id = uuid.uuid4()
        data, errors = self.schema.dump(data)

        self.assertFalse(errors)
        self.assertTrue("user" in data)

        user = data["user"]

        self.assertTrue("id" in user)
        self.assertTrue("e_mail" in user)
        self.assertTrue("create_stamp" not in user)
        self.assertTrue("edit_stamp" not in user)

        self.assertTrue("_links" in user)

        links = user["_links"]

        self.assertTrue("self" in links)
        self.assertTrue("collection" in links)


if __name__ == "__main__":
    unittest.main()
