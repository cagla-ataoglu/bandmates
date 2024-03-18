import boto3
import uuid
from botocore.exceptions import ClientError


class StorageService:
    def __init__(self):
        self.s3 = boto3.client('s3', endpoint_url='http://localstack:4566')

        self.bucket_name = 'bandmates-media-storage'
        try:
            self.s3.head_bucket(Bucket=self.bucket_name)
            print(f"Bucket {self.bucket_name} exists.")
        except ClientError as e:
            self.s3.create_bucket(Bucket=self.bucket_name)
            print(f"Bucket {self.bucket_name} created.")

    def upload_media(self, file_content, file_name):
        unique_file_name = f"{uuid.uuid4()}_{file_name}"
        self.s3.put_object(Bucket=self.bucket_name, Key=unique_file_name, Body=file_content)
        
        # URL Adress to media
        return f"http://localstack:4566/{self.bucket_name}/{unique_file_name}"
