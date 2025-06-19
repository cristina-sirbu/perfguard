import csv
import requests
import os

DISCORD_WEBHOOK=os.getenv("DISCORD_WEBHOOK")

def load_metrics(file):
    metrics = {}
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            key, value = row
            metrics[key] = float(value)
    return metrics

def send_discord_alert(message, success=True):
    if not DISCORD_WEBHOOK:
        print("No Discord webhook configured. Skipping alert.")
        return
    color = 3066993 if success else 15158332  # Green or Red
    payload = {
        "embeds": [
            {
                "title": "📊 PerfGuard Regression Check",
                "description": message,
                "color": color
            }
        ]
    }
    try:
        response = requests.post(DISCORD_WEBHOOK, json=payload)
        if response.status_code != 204:
            print(f"Failed to send Discord alert: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Exception sending Discord alert: {e}")

def detect_regression(baseline_file, latest_file, threshold_percent=10):
    baseline = load_metrics(baseline_file)
    latest = load_metrics(latest_file)

    p95_base = baseline["95th Percentile"]
    p95_latest = latest["95th Percentile"]

    increase = ((p95_latest - p95_base) / p95_base) * 100

    if increase > threshold_percent:
        msg = f"Regression Detected! p95 latency increased by {increase:.2f}%"
        print(msg)
        send_discord_alert(msg, success=False)
    else:
        msg = f"No regression. p95 latency change: {increase:.2f}%"
        print(msg)
        send_discord_alert(msg, success=True)

if __name__ == "__main__":
    detect_regression("baseline.csv", "latest_results.csv")
