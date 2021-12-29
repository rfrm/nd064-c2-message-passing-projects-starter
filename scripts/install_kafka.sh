
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install udaconnect-kafka -f ./deployment/values/kafka.yaml bitnami/kafka
