from locust import HttpUser, task, between, events
import time
import csv

class PerfGuardUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def login_and_search(self):
        self.client.post("/login", json={"user": "alice"})
        self.client.get("/search", params={"query": "test"})

# Hook: write stats to CSV after test
@events.test_stop.add_listener
def write_results(environment, **kwargs):
    stats = environment.runner.stats.total
    with open("latest_results.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Metric", "Value"])
        writer.writerow(["Request Count", stats.num_requests])
        writer.writerow(["Failures", stats.num_failures])
        writer.writerow(["Median Response Time", stats.median_response_time])
        writer.writerow(["95th Percentile", stats.get_response_time_percentile(0.95)])