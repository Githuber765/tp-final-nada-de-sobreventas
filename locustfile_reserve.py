from locust import HttpUser, task, between


class ReserveUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def reserve_product(self):
        with self.client.post(
            "/reserve",
            json={
                "product_id": 1,
                "quantity": 1
            },
            timeout=5,
            catch_response=True
        ) as response:

            if response.status_code == 200:
                response.success()

            elif response.status_code == 400:
                response.success()

            elif response.status_code == 503:
                response.success()

            else:
                response.failure(f"Error inesperado: {response.status_code}")