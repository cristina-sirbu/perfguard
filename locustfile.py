from locust import HttpUser, task, between

class PerfGuardUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def login_and_search(self):
        self.client.post("/login", json={"user": "alice"})
        self.client.get("/search", params={"query": "test"})
