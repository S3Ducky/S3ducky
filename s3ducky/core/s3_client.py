# MIT License
# 
# Copyright (c) 2025 S3Ducky

"""
S3 client and connection management for S3Ducky.
"""

import boto3
from boto3.session import Session
from botocore.exceptions import ClientError, NoCredentialsError, BotoCoreError


class S3Client:
    """
    Handles S3 connection and basic operations.
    """
    
    def __init__(self):
        self.session = None
        self.s3_client = None
        self.s3_resource = None
        self.bucket_name = ""
        self.resource_prefix = None
        
    def connect(self, access_key, secret_key, region, bucket_name, resource_prefix=None):
        """
        Connect to S3 using provided credentials.
        
        Args:
            access_key (str): AWS Access Key ID
            secret_key (str): AWS Secret Access Key
            region (str): AWS region
            bucket_name (str): S3 bucket name
            resource_prefix (str, optional): Prefix filter for objects
            
        Returns:
            bool: True if connection successful, False otherwise
            
        Raises:
            NoCredentialsError: Invalid AWS credentials
            ClientError: AWS service errors
            Exception: Other connection errors
        """
        # Validate inputs
        if not all([access_key, secret_key, region, bucket_name]):
            raise ValueError("All connection parameters are required")
            
        try:
            # Create S3 session and resource (more reliable than client for listing)
            self.session = Session(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region
            )
            
            # Create both client and resource for different operations
            self.s3_client = self.session.client('s3')
            self.s3_resource = self.session.resource('s3')
            
            # Store connection details
            self.bucket_name = bucket_name
            # Only use prefix if it's not empty and not just whitespace
            resource_input = resource_prefix.strip() if resource_prefix else ""
            self.resource_prefix = resource_input if resource_input else None
            
            # Test connection by attempting to list objects
            self._test_connection()
            
            return True
            
        except Exception as e:
            # Clean up on failure
            self.disconnect()
            raise e
    
    def _test_connection(self):
        """
        Test the S3 connection by attempting to list objects.
        
        Raises:
            ClientError: If bucket doesn't exist or access denied
        """
        try:
            # Try to list objects (limit to 1 for quick test)
            params = {'Bucket': self.bucket_name, 'MaxKeys': 1}
            if self.resource_prefix:
                params['Prefix'] = self.resource_prefix
            
            self.s3_client.list_objects_v2(**params)
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchBucket':
                raise ClientError(
                    error_response={'Error': {'Code': 'NoSuchBucket', 
                                            'Message': f"Bucket '{self.bucket_name}' does not exist"}},
                    operation_name='list_objects_v2'
                )
            elif error_code == 'AccessDenied':
                raise ClientError(
                    error_response={'Error': {'Code': 'AccessDenied', 
                                            'Message': "Access denied. Check your credentials and permissions"}},
                    operation_name='list_objects_v2'
                )
            else:
                raise e
    
    def disconnect(self):
        """
        Disconnect from S3 and clean up resources.
        """
        self.session = None
        self.s3_client = None
        self.s3_resource = None
        self.bucket_name = ""
        self.resource_prefix = None
    
    def is_connected(self):
        """
        Check if currently connected to S3.
        
        Returns:
            bool: True if connected, False otherwise
        """
        return self.s3_client is not None and self.bucket_name
    
    def list_objects(self):
        """
        List all objects in the connected bucket with optional prefix filter.
        
        Returns:
            list: List of object dictionaries with keys: 'key', 'size', 'modified'
            
        Raises:
            RuntimeError: If not connected to S3
            Exception: If listing fails
        """
        if not self.is_connected():
            raise RuntimeError("Not connected to S3. Call connect() first.")
        
        try:
            files_list = []
            
            print(f"Debug: Loading files from bucket: {self.bucket_name}")
            if self.resource_prefix:
                print(f"Debug: Using prefix filter: {self.resource_prefix}")
            
            # Use client method with pagination (most reliable)
            paginator = self.s3_client.get_paginator('list_objects_v2')
            
            # Set up pagination parameters
            page_params = {'Bucket': self.bucket_name}
            if self.resource_prefix:
                page_params['Prefix'] = self.resource_prefix
            
            page_iterator = paginator.paginate(**page_params)
            
            total_files = 0
            for page in page_iterator:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        total_files += 1
                        files_list.append({
                            'key': obj['Key'],
                            'size': obj['Size'],
                            'modified': obj['LastModified']
                        })
                        
                        # Log progress for large buckets
                        if total_files % 1000 == 0:
                            print(f"Debug: Loaded {total_files} files so far...")
            
            print(f"Debug: Successfully loaded {len(files_list)} files from S3")
            
            # Sort files by name
            files_list.sort(key=lambda x: x['key'])
            
            return files_list
            
        except Exception as e:
            print(f"Debug: Failed to load files: {str(e)}")
            raise Exception(f"Failed to load files: {str(e)}")
    
    def download_file(self, s3_key, local_path):
        """
        Download a single file from S3.
        
        Args:
            s3_key (str): S3 object key
            local_path (str): Local file path for download
            
        Raises:
            RuntimeError: If not connected to S3
            Exception: If download fails
        """
        if not self.is_connected():
            raise RuntimeError("Not connected to S3. Call connect() first.")
        
        try:
            self.s3_client.download_file(self.bucket_name, s3_key, local_path)
        except Exception as e:
            raise Exception(f"Failed to download {s3_key}: {str(e)}")
