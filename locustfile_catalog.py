from locust import HttpUser, task, between
import random

class CatalogUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(3)
    def list_products(self):
        # Target: < 100ms
        with self.client.get("/products", catch_response=True) as response:
            if response.elapsed.total_seconds() > 0.1:
                response.failure(f"Response time too high: {response.elapsed.total_seconds()}s")

    @task(7)
    def get_product(self):
        # Target: < 100ms
        # Assuming product IDs 1, 2, 3 exist based on startup seeding
        product_id = random.randint(1, 3)
        with self.client.get(f"/products/{product_id}", catch_response=True) as response:
            if response.elapsed.total_seconds() > 0.1:
                response.failure(f"Response time too high: {response.elapsed.total_seconds()}s")
