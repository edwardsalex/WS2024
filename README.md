# WS2024

GLHF! You'll be alright - Alex 2024-09-05

[EKS](EKS/helper.md)

[CodePipeline](CodePipeline/helper.md)

[rewritepathswithpython.py](Lambda@Edge/rewritepathswithpython.py)

[sqs-chaos-checker.yaml](build-sqs.yaml)



REMEMBER!!!!!!!!
- CloudFront deployment for caching
- S3 bucket versioning for EVERYTHING
- S3 bucket encryption enabled
- VPC Flow Logs (Just turn them on)
- Tag EVERYTHING
- CloudWatch
- Monitor Instances
- Monitor Load Balancer
- Security Groups
- Have NOTHING open to 0.0.0.0/0
- Triple check
- Any database solution will require encryption
- Any database solution will require backup
- Data in flight should use HTTPS
- Public/Private subnet. Bastion host to access private
- AutoScaling
- CP
