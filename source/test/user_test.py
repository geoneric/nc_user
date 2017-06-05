import os.path
import unittest
import uuid
from flask import current_app, json
from nc_user import create_app, db
from nc_user.api.schema import *


class UserTestCase(unittest.TestCase):


    def setUp(self):
        self.app = create_app("test")
        self.app.config["TESTING"] = True
        self.app.config["SERVER_NAME"] = "localhost"
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        self.user1 = {
            "id": uuid.uuid4(),
            "e_mail": "user1@domain1.org",
        }
        self.user2 = {
            "id": uuid.uuid4(),
            "e_mail": "user2@domain2.org",
        }
        self.user3 = {
            "id": uuid.uuid4(),
            "e_mail": "user3@domain3.org",
        }


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def post_user(self,
            payload):

        response = self.client.post("/users",
            data=json.dumps({"user": payload}),
            content_type="application/json")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 201, "{}: {}".format(
            response.status_code, data))

        return response


    def post_users(self):

        payloads = [
            {
                "id": self.user1["id"],
                "e_mail": self.user1["e_mail"],
            },
            {
                "id": self.user2["id"],
                "e_mail": self.user2["e_mail"],
            },
        ]

        for payload in payloads:
            self.post_user(payload)


    def test_get_all_users1(self):
        # No users posted.
        response = self.client.get("/users")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("users" in data)
        self.assertEqual(data["users"], [])


    def test_get_all_users2(self):
        # Some users posted.
        self.post_users()

        response = self.client.get("/users")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("users" in data)

        users = data["users"]

        self.assertEqual(len(users), 2)


    def test_get_user(self):
        self.post_users()

        response = self.client.get("/users")
        data = response.data.decode("utf8")
        data = json.loads(data)
        users = data["users"]
        user = users[0]
        uri = user["_links"]["self"]
        response = self.client.get(uri)

        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("user" in data)

        user = data["user"]

        self.assertEqual(data["user"], user)

        self.assertTrue("create_stamp" not in user)
        self.assertTrue("edit_stamp" not in user)

        self.assertTrue("id" in user)
        self.assertEqual(user["id"], str(self.user1["id"]))

        self.assertTrue("_links" in user)

        links = user["_links"]

        self.assertTrue("self" in links)
        self.assertEqual(links["self"], uri)

        self.assertTrue("collection" in links)


    def test_get_unexisting_user(self):
        self.post_users()

        response = self.client.get("/users")
        data = response.data.decode("utf8")
        data = json.loads(data)
        users = data["users"]
        user = users[0]
        uri = user["_links"]["self"]
        # Invalidate uri
        uri = os.path.join(os.path.split(uri)[0], str(uuid.uuid4()))
        response = self.client.get(uri)

        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 400, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


    def test_post_user(self):
        response = self.post_user(self.user3)

        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 201, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("user" in data)

        user = data["user"]

        self.assertTrue("create_stamp" not in user)
        self.assertTrue("edit_stamp" not in user)

        self.assertTrue("id" in user)
        self.assertEqual(user["id"], str(self.user3["id"]))

        self.assertTrue("e_mail" in user)
        self.assertEqual(user["e_mail"], self.user3["e_mail"])

        self.assertTrue("_links" in user)

        links = user["_links"]

        self.assertTrue("self" in links)
        self.assertTrue("collection" in links)


    def test_delete_user(self):
        response = self.post_user(self.user3)
        data = response.data.decode("utf8")
        data = json.loads(data)
        user = data["user"]
        links = user["_links"]
        self_uri = links["self"]

        response = self.client.delete(self_uri)
        data = response.data.decode("utf8")
        print(data)

        self.assertEqual(response.status_code, 204)


    def test_post_bad_request(self):
        response = self.client.post("/users")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 400, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


    def test_post_unprocessable_entity(self):
        payload = ""
        response = self.client.post("/users",
            data=json.dumps({"user": payload}),
            content_type="application/json")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 422, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


if __name__ == "__main__":
    unittest.main()
