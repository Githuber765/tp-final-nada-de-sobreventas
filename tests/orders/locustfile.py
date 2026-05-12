from locust import HttpUser, task, between
import random

class OrdersUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(2)
    def create_order(self):
        # Target: < 200ms
        with self.client.post("/orders", json={
            "items": [
                {"product_id": random.randint(1, 10), "quantity": random.randint(1, 5), "price": 10.0}
            ]
        }, catch_response=True) as response:
            if response.elapsed.total_seconds() > 0.2:
                response.failure(f"Response time too high: {response.elapsed.total_seconds()}s")

    @task(3)
    def get_order(self):
        # Target: < 200ms
        # Testing with random ID, might 404 which is acceptable for testing load on the DB/API
        order_id = random.randint(1, 100)
        with self.client.get(f"/orders/{order_id}", catch_response=True) as response:
            if response.elapsed.total_seconds() > 0.2:
                response.failure(f"Response time too high: {response.elapsed.total_seconds()}s")
