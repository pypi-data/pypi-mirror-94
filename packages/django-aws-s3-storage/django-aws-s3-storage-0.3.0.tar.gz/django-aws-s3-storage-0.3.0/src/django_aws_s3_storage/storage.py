import boto3

from botocore.exceptions import ClientError

from io import BytesIO

from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible

from django_aws_s3_storage.settings import app_settings
from django_aws_s3_storage.utils import create_file_public_url


@deconstructible
class S3Storage(Storage):

    def __init__(self):
        self.client = boto3.client(
            's3',
            aws_access_key_id=app_settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=app_settings.AWS_SECRET_ACCESS_KEY,
        )

    def _open(self, name, mode='rb'):
        obj = self.client.get_object(
            Bucket=app_settings.BUCKET_NAME,
            Key=name,
        )
        return obj['Body']

    def _save(self, name, content):
        # Always change the stream position to the beginning of the file
        content.seek(0)
        # Save the file in memory temporarily
        temp_file = BytesIO()

        for chunk in content.chunks():
            temp_file.write(chunk)

        self.client.put_object(
            Bucket=app_settings.BUCKET_NAME,
            Body=temp_file.getvalue(),
            Key=name,
            ContentType=content.content_type,
        )
        # Close the buffer of the file stored in memory
        temp_file.close()
        return name

    def delete(self, name):
        self.client.delete_object(Bucket=app_settings.BUCKET_NAME, Key=name)
        return name

    def exists(self, name):
        try:
            self.client.head_object(Bucket=app_settings.BUCKET_NAME, Key=name)
        except ClientError:
            return False
        return True

    def url(self, name):
        if app_settings.PUBLIC_URL != '':
            return create_file_public_url(app_settings.PUBLIC_URL, name)
        return self.client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': app_settings.BUCKET_NAME,
                'Key': name,
            },
            ExpiresIn=app_settings.MAX_AGE_SECONDS,
        )
