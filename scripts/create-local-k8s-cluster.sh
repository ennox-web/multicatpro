cluster_file=".\config\local\cluster.yaml"
cluster_name="multicat"

secrets_folder=".\config\local\secrets\."
backend_folder=".\config\backend\."
frontend_folder=".\config\frontend\."

kind delete cluster --name=${cluster_name}
kind create cluster --config=${cluster_file}

kubectl apply -f ${secrets_folder}
kubectl apply -f ${backend_folder}
# kubectl apply -f ${frontend_folder}