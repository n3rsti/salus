from locust import HttpUser, task, between
import random
import string

def random_email():
    return "".join(random.choices(string.ascii_lowercase, k=8)) + "@test.com"

class RegisterUser(HttpUser):
    wait_time = between(0.5, 2)

    @task
    def register_user(self):
        self.client.post(
            "/api/users",
            json={
                "username": "user_" + "".join(random.choices(string.ascii_lowercase, k=6)),
                "email": random_email(),
                "password": "Password1234*",
                "role_id": 1
            }
        )
