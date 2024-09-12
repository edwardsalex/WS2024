Some best practices:

## 1. Cost Management
- Use PrivateLink to reduce inter-VPC costs

## 2. Security
- Use multiple subnets (pub/priv) in order to logically isolate instances
- Ensure SGs and ACLs are properly implemented. DO NOT 0.0.0.0/0 ANYTHING!!!!
- Monitor using VPC flow logs, just turn them on for both ACCEPT and DENY.
- Use private endpoints to avoid transferring data over hostile net
- Encrypt over wire (SSL/TLS), and KMS for resting data
