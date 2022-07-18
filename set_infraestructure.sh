cd infraestructure/aws
terraform init
terraform validate 
terraform apply --var-file=terraform.tfvars 
aws eks --region $(terraform output -raw region) update-kubeconfig --name $(terraform output -raw cluster_name)
export NFS_SERVER=$(terraform output -raw efs)
cd ../kubernetes
kubectl create namespace storage
helm repo add nfs-subdir-external-provisioner https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner/
helm install nfs-subdir-external-provisioner nfs-subdir-external-provisioner/nfs-subdir-external-provisioner \
    --namespace storage \
    --set nfs.server=$NFS_SERVER \
    --set nfs.path=/
kubectl create namespace airflow
helm repo add apache-airflow https://airflow.apache.org
helm install airflow -f airflow-values.yaml apache-airflow/airflow --namespace airflow
kubectl get pods -n airflow