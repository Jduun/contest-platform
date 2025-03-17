import json
import os
from contextlib import asynccontextmanager

from aiobotocore.session import get_session
from fastapi import UploadFile


class S3Client:
    def __init__(
        self, access_key: str, secret_key: str, endpoint_url: str, bucket_name: str
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_s3_client(self):
        async with self.session.create_client(
            "s3",
            **self.config,
            # use_ssl=False, verify=False, region_name="us-east-1"
        ) as s3_client:
            yield s3_client

    async def upload_file(self, file: UploadFile, key: str) -> str:
        async with self.get_s3_client() as s3_client:
            try:
                await s3_client.create_bucket(Bucket=self.bucket_name)
            except Exception:
                pass
            public_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": "s3:GetObject",
                        "Resource": f"arn:aws:s3:::{self.bucket_name}/*",
                    }
                ],
            }
            await s3_client.put_bucket_policy(
                Bucket=self.bucket_name, Policy=json.dumps(public_policy)
            )
            await s3_client.put_object(
                Bucket=self.bucket_name, Key=key, Body=await file.read()
            )
        url = f"http://localhost:{os.getenv('MINIO_PORT')}/{self.bucket_name}/{key}"
        return url

    async def check_file(self, filename: str) -> bool:
        try:
            async with self.get_s3_client() as s3_client:
                await s3_client.head_object(Bucket=self.bucket_name, Key=filename)
                return True
        except s3_client.exceptions.ClientError:
            return False


avatar_s3_client = S3Client(
    os.getenv("MINIO_ACCESS_KEY"),
    os.getenv("MINIO_SECRET_KEY"),
    f"http://{os.getenv('MINIO_HOST')}:{os.getenv('MINIO_PORT')}",
    "avatars",
)
