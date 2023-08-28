# argo-s3-mlops-pipeline
Add Argo Workflows 
```
helm repo add argo https://argoproj.github.io/argo-helm
kubectl create ns argo
helm install --namespace argo my-argo-workflows argo/argo-workflows --version 0.22.8

kubectl create role app --verb="*" --resource=workflows.argoproj.io --namespace argo
kubectl create sa app --namespace argo
kubectl create rolebinding app --role=app --serviceaccount=argo:app --namespace argo

kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: app.service-account-token
  namespace: argo
  annotations:
    kubernetes.io/service-account.name: app
type: kubernetes.io/service-account-token
EOF

ARGO_TOKEN="Bearer $(kubectl get -n argo secret app.service-account-token -o=jsonpath='{.data.token}' | base64 --decode)"
```
Get Argo Workflows Access Token
```
echo $ARGO_TOKEN
```

Paste token into `velocity-values.yaml`

```
minikube image pull jdvincent/ml-image-to-tensor-s3-workflow:latest
```

Create AWS Credentials Secret in argo namespace
```
kubectl create secret generic -n argo aws-credentials \
    --from-literal=aws_access_key_id=<your-access-key-id> \
    --from-literal=aws_secret_access_key=<your-secret-access-key> \
    --from-literal=aws_session_token=<your-session-token>
```

Deploy CronJob
```
helm template . -f values.yaml | kubectl apply -f -
```

