cluster_file=".\k8s-config\local\cluster.yaml"
cluster_name="multicat"

secrets_folder=".\k8s-config\local\secrets\."
backend_folder=".\k8s-config\backend\."
frontend_folder=".\k8s-config\frontend\."

kind delete cluster --name=${cluster_name}
kind create cluster --config=${cluster_file}

kubectl apply -f ${secrets_folder}
kubectl apply -f ${backend_folder}
# kubectl apply -f ${frontend_folder}