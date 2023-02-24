# argo-s3-mlops-pipeline

```
helm repo add argo https://argoproj.github.io/argo-helm
helm install my-argo-workflows argo/argo-workflows --version 0.22.8

kubectl create role app --verb="*" --resource=workflows.argoproj.io
kubectl create sa app
kubectl create rolebinding app --role=app --serviceaccount=default:app

kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: app.service-account-token
  annotations:
    kubernetes.io/service-account.name: app
type: kubernetes.io/service-account-token
EOF

ARGO_TOKEN="Bearer $(kubectl get secret app.service-account-token -o=jsonpath='{.data.token}' | base64 --decode)"
```

```
echo $ARGO_TOKEN
```

