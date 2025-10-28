## 🚀 **End-to-End ML Observability Stack**
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)
![Helm](https://img.shields.io/badge/Helm-0F1689?style=for-the-badge&logo=helm&logoColor=white)

This project builds a complete, production-style monitoring pipeline for a machine learning application. It uses a **Flask** app to expose metrics, which is then containerized by **Docker** and deployed on **Kubernetes** (Minikube). The entire stack is monitored using **Prometheus** for data scraping and **Grafana** for visualization, all managed reproducibly with **Helm** charts.

***

### 🛠️ **Project Highlights**

* **Full Observability Stack**: A complete setup from metrics exposure (Flask) to collection (Prometheus) and visualization (Grafana).
* **Kubernetes Deployment**: Deploys the application as a containerized service on Minikube, simulating a production-ready environment.
* **Declarative & Reproducible**: Uses Kubernetes manifests (`flask-app.yaml`) and Helm charts for an easy-to-replicate infrastructure.
* **Isolated Monitoring**: Deploys Prometheus and Grafana into a separate `monitoring` namespace for a clean separation of concerns from the application.

***

### 🧠 **Core Workflow**

1.  **Application**: A Python **Flask** app (`app.py`) serves the application and exposes custom metrics (e.g., `total_api_requests_total`) on a `/metrics` endpoint.
2.  **Containerization**: The app is containerized using **Docker** into an image (`ml-metrics-flask-app:latest`) and loaded directly into the Minikube cluster.
3.  **Deployment**: The container is deployed to Kubernetes using a manifest file (`flask-app.yaml`), which defines the `Deployment` and a `NodePort` `Service` to make the app accessible.
4.  **Metrics Collection**: **Prometheus** is installed via Helm. Its `ConfigMap` is then manually edited to add the Flask app's service as a scrape target, allowing Prometheus to pull metrics.
5.  **Visualization**: **Grafana** is installed via Helm. It is configured inside its UI to use the internal Prometheus service (`http://prometheus-server.monitoring.svc.cluster.local:80`) as its primary data source.

***

### 📈 **Accessing the Monitoring Stack**

After deployment, the services are not exposed publicly by default. Use `kubectl port-forward` to access them on your `localhost`.

| Service | Namespace | Command | Access URL |
| :--- | :---: | :--- | :--- |
| **Prometheus** | `monitoring` | `kubectl port-forward -n monitoring svc/prometheus-server 9090:80` | `http://localhost:9090` |
| **Grafana** | `monitoring` | `kubectl port-forward svc/grafana -n monitoring 3000:80` | `http://localhost:3000` |
| **Flask App** | `default` | `minikube service ml-metrics-flask-app --url` | (URL provided by command) |

#### **Grafana Credentials**

* **Username**: `admin`
* **Password**: Run the following command to retrieve the auto-generated password:
    ```sh
    kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
    ```

***

### 📊 **Visualization Dashboard**

Once Grafana is connected to the Prometheus data source, you can build dashboards to visualize your application's metrics in real-time, such as API request counts, error rates, or model performance.

![Grafana Dashboard Placeholder](grafana-dashboard.png)

> A placeholder for a custom Grafana dashboard monitoring the Flask app's metrics.

### ⚙️ **Tech Stack**

* **Application**: `Flask`, `Python`
* **Containerization**: `Docker`
* **Orchestration**: `Kubernetes (Minikube)`
* **Monitoring**: `Prometheus`
* **Visualization**: `Grafana`
* **Package Management**: `Helm`

***

### ▶️ **How to Run**

1.  **Start Minikube:**
    ```sh
    minikube start
    ```
2.  **Build & Load Docker Image:**
    ```sh
    docker build -t ml-metrics-flask-app:latest .
    minikube image load ml-metrics-flask-app:latest
    ```
3.  **Deploy the Flask Application:**
    ```sh
    kubectl apply -f flask-app.yaml
    ```
4.  **Add Helm Repos:**
    ```sh
    helm repo add prometheus-community [https://prometheus-community.github.io/helm-charts](https://prometheus-community.github.io/helm-charts)
    helm repo add grafana [https://grafana.github.io/helm-charts](https://grafana.github.io/helm-charts)
    helm repo update
    ```
5.  **Install Prometheus & Grafana:**
    ```sh
    helm install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace
    helm install grafana grafana/grafana -n monitoring --create-namespace
    ```
6.  **Configure Prometheus to Scrape App:**
    * Find your app's service address: `kubectl get svc ml-metrics-flask-app` (Note the ClusterIP and Port).
    * Edit the Prometheus ConfigMap: `kubectl edit configmap prometheus-server -n monitoring`
    * Add a new `job_name` under `scrape_configs` to target your app's service (e.g., `<cluster-ip>:<port>`).
    * Restart the Prometheus deployment to apply changes:
        ```sh
        kubectl rollout restart deployment prometheus-server -n monitoring
        ```
7.  **Access Services:**
    * Use the `kubectl port-forward` commands from the "Accessing the Monitoring Stack" section above.
    * Log in to Grafana, add Prometheus as a data source, and start building dashboards.