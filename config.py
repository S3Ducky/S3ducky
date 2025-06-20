# S3 Bucket Viewer Configuration
# This file contains example configuration and setup instructions

# AWS Regions (choose the one closest to your bucket)
COMMON_AWS_REGIONS = [
    "us-east-1",      # US East (N. Virginia) - Default
    "us-west-2",      # US West (Oregon)
    "eu-west-1",      # Europe (Ireland)
    "eu-central-1",   # Europe (Frankfurt)
    "ap-southeast-1", # Asia Pacific (Singapore)
    "ap-northeast-1"  # Asia Pacific (Tokyo)
]

# Example AWS Credentials Setup
# DO NOT STORE ACTUAL CREDENTIALS IN THIS FILE!
EXAMPLE_CREDENTIALS = {
    "aws_access_key_id": "AKIAIOSFODNN7EXAMPLE",
    "aws_secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    "region_name": "us-east-1",
    "bucket_name": "my-example-bucket"
}

# Setup Instructions:
# 1. Create an AWS account if you don't have one
# 2. Go to AWS IAM (Identity and Access Management)
# 3. Create a new user with programmatic access
# 4. Attach the AmazonS3ReadOnlyAccess policy (or create custom policy)
# 5. Save the Access Key ID and Secret Access Key
# 6. Use these credentials in the application

# Minimum IAM Policy for S3 Bucket Access:
MINIMUM_IAM_POLICY = """
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::your-bucket-name",
                "arn:aws:s3:::your-bucket-name/*"
            ]
        }
    ]
}
"""

# Troubleshooting Tips:
TROUBLESHOOTING = """
Common Issues and Solutions:

1. "Invalid AWS credentials"
   - Double-check your Access Key ID and Secret Access Key
   - Ensure the IAM user has the necessary permissions

2. "Bucket does not exist"
   - Verify the bucket name is correct (case-sensitive)
   - Ensure the bucket is in the specified region

3. "Access denied"
   - Check that your IAM user has permissions to access the bucket
   - Verify the bucket policy allows your user to access it

4. "Connection timeout"
   - Check your internet connection
   - Verify the region is correct
   - Some corporate networks may block AWS API calls

5. "SSL Certificate errors"
   - This may occur on some corporate networks
   - Contact your IT administrator for assistance
"""
