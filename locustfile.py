from locust import HttpUser, task


class CartUser(HttpUser):
    @task
    def add_item_to_a_cart(self):
        self.client.post("items/", json={"external_id": "123123"})
