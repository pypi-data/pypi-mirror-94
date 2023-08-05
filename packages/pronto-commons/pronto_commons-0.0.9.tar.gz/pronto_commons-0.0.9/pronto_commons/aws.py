import io

import boto3


def upload_file_to_s3(*, access_key: str, secret_key:str, bucket_name: str, key: str, file: io.BytesIO):
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    s3 = session.resource("s3")
    attachment_file = s3.Bucket(bucket_name).put_object(
        Key=key, Body=file, ACL="public-read"
    )
    return attachment_file
