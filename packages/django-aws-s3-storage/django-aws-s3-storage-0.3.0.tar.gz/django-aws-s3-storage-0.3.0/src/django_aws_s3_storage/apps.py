from django.apps import AppConfig

from django_aws_s3_storage.settings import DjangoAWSS3StorageSettings


class DjangoAWSS3StorageConfig(AppConfig):
    name = 'django_aws_s3_storage'

    def ready(self):
        DjangoAWSS3StorageSettings.init()
