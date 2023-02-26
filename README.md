# argo-s3-mlops-pipeline

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

```
echo $ARGO_TOKEN
```

Paste token into `velocity-values.yaml`

```
minikube image pull jdvincent/ml-image-to-tensor-s3-workflow:latest
```

```
helm template . -f velocity-values.yaml | veloctl env create -f -
```

