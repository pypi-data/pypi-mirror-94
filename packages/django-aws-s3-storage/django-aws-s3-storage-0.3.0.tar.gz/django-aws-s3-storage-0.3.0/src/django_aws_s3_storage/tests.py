import boto3

from django.conf import settings
from django.test import TestCase

from io import BytesIO

from moto import mock_s3

from django_aws_s3_storage.settings import app_settings
from django_aws_s3_storage.storage import S3Storage


def create_s3_context():
    conn = boto3.resource('s3')
    conn.create_bucket(Bucket=app_settings.BUCKET_NAME)
    return conn


class ApplicationSettingsTestCase(TestCase):

    def test_application_must_be_well_configured(self):
        self.assertIn('django_aws_s3_storage', settings.INSTALLED_APPS)
        self.assertTrue(hasattr(settings, 'DJANGO_AWS_S3_STORAGE'))


class StorageTestCase(TestCase):
    storage = S3Storage()

    @mock_s3
    def test_uploaded_file_must_exist_on_bucket(self):
        create_s3_context()
        filename = 'random_file.txt'
        self.storage.save(filename, BytesIO())
        self.assertTrue(self.storage.exists(filename))
