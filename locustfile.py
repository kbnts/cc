import random
import string

from locust import HttpUser, task


class CartUser(HttpUser):
    @task
    def add_item_to_a_cart(self):
        letters = list(string.ascii_lowercase)
        self.client.post("items/", json={"external_id": f"hey-buddy-{random.choice(letters)}"})
