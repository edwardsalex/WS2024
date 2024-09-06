Set default region:
```
TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
export AWS_DEFAULT_REGION=$(curl -H "X-aws-ec2-metadata-token: $TOKEN" --silent http://169.254.169.254/latest/meta-data/placement/region)
echo $AWS_DEFAULT_REGION
```
Install tools and services:
```
#!/bin/bash
# Move to Cloud9 bootstrap
sudo yum update -y

# Get python version; need >= 3.7
eval $(python -c "import sys;print('major={} minor={} micro={}-{}-{}'.format(*sys.version_info))")
if [ $major -ne 3 -o $minor -lt 7 ]; then
     # Update python
     sudo yum install python38 -y
     # Get python 3.8 from the linux-extras
     sudo amazon-linux-extras install python3.8 -y
fi
# Install pip
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user

# Replace AWS CLI with V2 latest version
rm -rf /usr/bin/aws
sudo rm -rf /usr/bin/aws /usr/local/aws-cli/v2/current
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install -b
echo 'export PATH=$PATH:/usr/bin/aws' >> ~/.bashrc

# Create bin directory in $HOME
mkdir -p $HOME/bin && export PATH=$PATH:$HOME/bin
echo 'export PATH=$PATH:$HOME/bin' >> ~/.bashrc

## Install kubectl
curl -LO -o kubectl https://s3.us-west-2.amazonaws.com/amazon-eks/1.26.4/2023-05-11/bin/linux/amd64/kubectl
chmod +x ./kubectl
cp ./kubectl $HOME/bin/kubectl
# Test version
$HOME/bin/kubectl version --client --short

# Install aws-iam-authenticator
curl -o aws-iam-authenticator https://s3.us-west-2.amazonaws.com/amazon-eks/1.21.2/2021-07-05/bin/linux/amd64/aws-iam-authenticator
chmod +x ./aws-iam-authenticator
cp ./aws-iam-authenticator $HOME/bin/aws-iam-authenticator
$HOME/bin/aws-iam-authenticator version

## Install eksctl
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin
eksctl version

## Install helm
curl -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod 755 get_helm.sh
./get_helm.sh
helm version

. ~/.bashrc
hash -r
```
Create EKS Cluster
```
eksctl create cluster \
--name <cluster-name> \
--nodegroup-name worknodes-1 \
--node-type t3.medium \
--nodes 2 \
--nodes-min 1 \
--nodes-max 4 \
--managed \
--version 1.29 \
--region ${AWS_DEFAULT_REGION}
```
If any of these outputs are seen:
- ```Unable to connect to the server: getting credentials: decoding stdout: no kind “ExecCredential” is registered for version “client.authentication.k8s.io/v1alpha1” in scheme “pkg/client/auth/exec/exec.go:62”```

- ```Unable to use kubectl with the EKS cluster (check ‘kubectl version’): WARNING: This version information is deprecated and will be replaced with the output from kubectl version --short.```

- ```Getting Kubernetes version on EKS cluster: error running kubectl version: exit status 1 (check ‘kubectl version’)```

Then run ```aws eks update-kubeconfig --name <cluster-name> --region ${AWS_DEFAULT_REGION}``` to fix.

Once done, build docker containers then push to ECR, then:

```
echo "export AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}" >> ~/.bash_profile
source ~/.bash_profile
aws configure set default.region $AWS_DEFAULT_REGION
```
Then repeat ```aws eks update-kubeconfig --name <cluster-name> --region ${AWS_DEFAULT_REGION}``` to update the kubernetes configuration.

To build the ALB controller, do:
```
#!/bin/bash
# Set ACCOUNT_NUMBER vairable
export ACCOUNT_NUMBER=$(aws sts get-caller-identity --query 'Account' --output text)
# Create an IAM OIDC (Open ID Connect) provider
echo "Running: eksctl utils associate-iam-oidc-provider --region us-west-2 --cluster <cluster-name> --approve"
eksctl utils associate-iam-oidc-provider --region us-west-2 --cluster <cluster-name> --approve
# Create a Kubernetes service account named aws-load-balancer-controller in the kube-system namespace for the AWS Load Balancer Controller and annotate the Kubernetes service account with the name of the IAM role.
echo "Running: eksctl create iamserviceaccount --cluster=<cluster-name> --namespace=kube-system --name=aws-load-balancer-controller --role-name "AmazonEKSLoadBalancerControllerRole" --attach-policy-arn=arn:aws:iam::$ACCOUNT_NUMBER:policy/AWSLoadBalancerControllerIAMPolicy --approve"
eksctl create iamserviceaccount --cluster=<cluster-name> --namespace=kube-system --name=aws-load-balancer-controller --role-name "AmazonEKSLoadBalancerControllerRole" --attach-policy-arn=arn:aws:iam::$ACCOUNT_NUMBER:policy/AWSLoadBalancerControllerIAMPolicy --approve
sleep 5
# Add helm eks-charts repository
echo "Running: helm repo add eks https://aws.github.io/eks-charts"
helm repo add eks https://aws.github.io/eks-charts
# helm update
echo "Running: helm repo update"
helm repo update
# Install the AWS Load Balancer Controller.
## Reference: https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html
echo "Running: helm install aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system --set clusterName=<cluster-name> --set serviceAccount.create=false --set serviceAccount.name=aws-load-balancer-controller"
helm install aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system --set clusterName=<cluster-name> --set serviceAccount.create=false --set serviceAccount.name=aws-load-balancer-controller
```

CREATE A DIFFERENT NAMESPACE: ```kubectl create namespace <namespace-name>```

Example ```k8s.yaml``` service file:
```
apiVersion: apps/v1
kind: Deployment
metadata:
  namespace: <namespace-name>
  name: eks-lab-deploy
  labels:
    app: eks-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: lab-app
  template:
    metadata:
      labels:
        app: lab-app
    spec:
      containers:
      - name: website
        image: $ECR_REPO_URI_WEBSITE:latest ## <-- Placeholder replaced with environment variable
        ports:
        - containerPort: 80
        volumeMounts:
        - mountPath: /var/metadata
          name: metadata-vol
      - name: sidecar
        image: $ECR_REPO_URI_SIDECAR:latest ## <-- Placeholder replaced with environment variable
        volumeMounts:
        - mountPath: /var/metadata
          name: metadata-vol
      volumes:
      - name: metadata-vol
        emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: lab-service
  namespace: containers-lab
spec:
  ports:
    - port: 80
      targetPort: 80
      protocol: TCP
  type: NodePort
  selector:
    app: lab-app
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  namespace: containers-lab
  name: lab-ingress
  annotations:
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    kubernetes.io/ingress.class: alb
spec:
  rules:
    - http:
        paths:
        - path: /
          pathType: Prefix
          backend:
            service:
              name: lab-service
              port:
                number: 80
```

In order to create this service based on a file, do:
```
kubectl apply -f <file.yaml>
```

To create a IAM role for the EKS pods to communicate with API calls:
```
eksctl create iamserviceaccount \
    --name iampolicy-sa \
    --namespace <namespace-name> \
    --cluster <cluster-name> \
    --role-name "eksRole4serviceaccount" \
    --attach-policy-arn arn:aws:iam::$ACCOUNT_NUMBER:policy/eks-lab-read-policy \
    --approve \
    --override-existing-serviceaccounts
```
Then:
```
kubectl get sa iampolicy-sa -n <namespace-name> -o yaml
```
To make sure a service account policy is set, then:
```
kubectl set serviceaccount \
 deployment eks-lab-deploy \
 iampolicy-sa -n <namespace-name>
```

See: https://aws.github.io/aws-eks-best-practices/security/docs/detective/ for more information.
