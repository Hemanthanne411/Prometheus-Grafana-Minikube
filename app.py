from flask import Flask, jsonify, render_template
import random
import time

app = Flask(__name__)

# Simulated metrics 
# Total rewuests to the app, request procesing latency(random), and model prediction success rate(random)
total_requests = 0

# The metrics endpoint for prometheus to scrape
@app.route("/metrics", methods=["GET"])
def metrics():
    global total_requests
    total_requests += 1

    # Simulated values
    request_processing_latency = round(random.uniform(0.1, 1.5), 3)  # Latency in seconds
    model_training_accuracy_score = round(random.uniform(80, 100), 2)  # Success rate in %

    # To Return the metrics in Prometheus format
    prometheus_metrics = (
        # Metric 1
        f"# HELP total_api_requests_total Total number of API requests\n"
        f"# TYPE total_api_requests_total counter\n"
        f"total_api_requests_total {total_requests}\n"
        # Metric 2
        f"\n"
        f"# HELP request_processing_latency_seconds Latency for request processing\n"
        f"# TYPE request_processing_latency_seconds gauge\n"
        f"request_processing_latency_seconds {request_processing_latency}\n"
        # Metric 3
        f"\n"
        f"# HELP model_training_accuracy_score Model prediction success rate\n"
        f"# TYPE model_training_accuracy_score gauge\n"
        f"model_training_accuracy_score {model_training_accuracy_score}\n"
    )

    return prometheus_metrics, 200, {"Content-Type": "text/plain; charset=utf-8"}

# Main route
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6006)