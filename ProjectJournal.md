# Created app.py with simulated ML application metrics.

- Verified the simple application on localhost.
- Kubernetes manifest yaml file with service and deployment specification 
    - To give the image locally.
    - port 6006, Type NodePort - to acess the application from outside of the minikube cluster.
- Built a docker image "ml-metrics-flask-app:latest" to containerize the app.



# Started minikube cluster

- Added the application image to the cluster:
    minikube image load ml-metrics-flask-app:latest

- Verifying if the app is running successfully inside the cluster -> Yes
    kubectl apply -f flask-app.yaml
    minikube service ml-metrics-flask-app --url
    -> Accessing the application from outside using NodePort was successful

# INSTALLIN PROMETHEUS using HELM

- installed helm,
    - to add prometheus to helm repo:
     "helm repo add prometheus-community https://prometheus-community.github.io/helm-charts"
     "helm repo update"

    - Installing Prometheus inside the cluster using helm:
        "helm install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace"
        **Seperating the namespace in order to isolate monitoring and application

    - Adding Prometheus two ways:
    1)
    --Get the pod name and add it to env variable 
        export POD_NAME=$(kubectl get pods --namespace monitoring -l "app.kubernetes.io/name=prometheus,app.kubernetes.io/instance=prometheus" -o jsonpath="{.items[0].metadata.name}")
    --Port Forwarding the pod to 9090 (prometheus port)
        kubectl --namespace monitoring port-forward $POD_NAME 9090
    2) 
    - kubectl get svc -n monitoring 
     to get the services in monitoring namespace : all the prometheus ones
    - kubectl port-forward -n monitoring svc/prometheus-server 9090:80
     to portforward the server to localhost

# ADDING THE APPLICATION'S METRICS PAGE TO PROMETHEUS CONFIG YAML for prometheus to track:

- As we cannot access the ui (yaml) of the prometheus config;
    1) Noting down the applications adress:port (flask-metrics-app   NodePort    10.100.146.231   <none>        6006:32040/TCP   42m)
        10.100.146.231:6006:32040/TCP
    2)  **Now adding the adress to prometheus's configmap to allow it to track.**
        "kubectl edit configmap prometheus-server -n monitoring"
        **Then restart (rolling) the prometheus deployment.**
        "kubectl rollout restart deployment prometheus-server -n monitoring"
        Forward the port:
        "kubectl port-forward -n monitoring svc/prometheus-server 9090:80"



# INSTALLIN Grafana Inside the minikube CLuster

- the command to add the grafana chart to repo:
    "helm repo add grafana https://grafana.github.io/helm-charts"
    "helm repo update"

- Then adding grafana to the cluster using helm (the nameapce is still MONITORING - same as that of prometheus)
    "helm install grafana grafana/grafana -n monitoring --create-namespace"

- Verifying the installation of grafana or prometheus inside the cluster:
    PODS: kubectl get pods -n monitoring
    SERVICE: kubectl get svc -n monitoring

- Port Forwarding to localhost:
    kubectl port-forward svc/grafana -n monitoring 3000:80

-   Username : admin  , Password: qI6jt4Y2YpByy4rTdjV2wIgYuoa9tlOM4Uhp7k4q

    Get the password from the given command:kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}  " | base64 --decode ; echo

- Add prometheus as a datasource with **GET method** :
    http://prometheus-server.monitoring.svc.cluster.local:80
    (svc.cluster.local → default Kubernetes cluster domain. This is the standard suffix for Services inside the cluster)

