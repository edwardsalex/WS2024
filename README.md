# WS2024

GLHF! You'll be alright - Alex 2024-09-05

[EKS](EKS/helper.md)

[CodePipeline](CodePipeline/helper.md)

[rewritepathswithpython.py](Lambda@Edge/rewritepathswithpython.py)

[sqs-chaos-checker.yaml](build-sqs.yaml)



MUST HAVES/MUST DO
● CloudFront deployment for caching
● S3 bucket versioning for EVERYTHING
● S3 bucket encryption enabled
● VPC Flow Logs (Just turn them on)
● Tag EVERYTHING
● CloudWatch
● Monitor Instances
● Monitor Load Balancer
● Security Groups
● Have NOTHING open to 0.0.0.0/0
● Triple check
● Any database solution will require encryption
● Any database solution will require backup
● Data in flight should use HTTPS
● Public/Private subnet. Bastion host to access private
● AutoScaling
● CP
Create something w/ DynamoDB, Lambda, Endpoint Gateway
Step 1 (BUILD VPC):
● CloudWatch
● VPC Flow Logs (Just turn them on)
Step 2 (CREATE S3):
● S3 bucket versioning for EVERYTHING
● S3 bucket encryption enabled
Step 3 (CREATE BASTION):
● Public/Private subnet. Bastion host to access private
● Monitor Instances
