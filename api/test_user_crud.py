import unittest, json
from  user_crud import create_app
from requests.auth import  _basic_auth_str
import random
import string



# user crud operations test
class UserTest(unittest.TestCase):

    def random_user(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5))


    def setUp(self):
        self.user = self.random_user()
        app = create_app()
        self.client =app.test_client()


    def test_create_user(self):
        payload = {
            "username":self.user,
            "email":self.user+"@gmail.com"
        }
        headers = {"Content-Type": "application/json", 'Authorization': _basic_auth_str(username="admin", password="password")}
        response = self.client.post('/users', headers=headers, data=json.dumps(payload))
        self.id = response.json["id"]
        self.assertEqual(200, response.status_code)
        self.assertEqual(payload["username"], response.json["username"])


        with self.subTest("get user"):
            response = self.client.get('/users/{}'.format(self.id), headers=headers)
            self.assertEqual(self.user, response.json["username"])


        with self.subTest("update user"):
            user = self.random_user()
            payload = {
            "username":user,
            "email":user+"@gmail.com"
            }

            headers = {"Content-Type": "application/json", 'Authorization': _basic_auth_str(username="admin", password="password")}
            r = self.client.put('/users/{}'.format(self.id), headers=headers, data=json.dumps(payload))
            response = self.client.get('/users/{}'.format(self.id), headers=headers)
            self.assertEqual(response.json["username"], payload["username"])


        with self.subTest("Delete user"):
            headers = {"Content-Type": "application/json", 'Authorization': _basic_auth_str(username="admin", password="password")}
            r = self.client.delete('/users/{}'.format(self.id), headers=headers)
            response = self.client.get('/users/{}'.format(self.id), headers=headers)
            self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
