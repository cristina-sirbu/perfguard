from prometheus_client import start_http_server, Gauge
import time
import csv

p95_latency = Gauge('perfguard_p95_latency', '95th percentile latency (ms)')
median_latency = Gauge('perfguard_median_latency', 'Median latency (ms)')
failures = Gauge('perfguard_failures', 'Number of failed requests')

def read_latest_results(file='latest_results.csv'):
    metrics = {}
    with open(file, newline='') as csvfile:
        next(csvfile)  # skip header
        for row in csv.reader(csvfile):
            key, value = row
            metrics[key] = float(value)
    return metrics

if __name__ == "__main__":
    start_http_server(9200)
    print("🔄 Exporting metrics on :9200")

    while True:
        try:
            metrics = read_latest_results()
            p95_latency.set(metrics.get("95th Percentile", 0))
            median_latency.set(metrics.get("Median Response Time", 0))
            failures.set(metrics.get("Failures", 0))
        except Exception as e:
            print("Could not read CSV:", e)
        time.sleep(5)
