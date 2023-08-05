from django.conf import settings
from django.utils.translation import gettext as _


DEFAULT_SETTINGS = {
    'AWS_ACCESS_KEY_ID': None,
    'AWS_SECRET_ACCESS_KEY': None,
    'BUCKET_NAME': None,
    'MAX_AGE_SECONDS': 60,
    'PUBLIC_URL': '',
}

NONE_SETTING_NULL_ERROR_MESSAGE = '{} setting can not be None.'

# If `None` DjangoAWSS3StorageSettings.init was never called
app_settings = None


class DjangoAWSS3StorageSettings(object):

    def _setup(self):
        app_settings = getattr(settings, 'DJANGO_AWS_S3_STORAGE', None)
        if app_settings is None:
            raise NameError(_(NONE_SETTING_NULL_ERROR_MESSAGE.format('DJANGO_AWS_S3_STORAGE')))

        for k, default_v in DEFAULT_SETTINGS.items():
            v = app_settings.get(k, default_v)
            if v is None:
                raise NameError(_(NONE_SETTING_NULL_ERROR_MESSAGE.format(f'DJANGO_AWS_S3_STORAGE.{k}')))
            setattr(self, k, v)

    def __init__(self):
        self._setup()

    @staticmethod
    def init():
        global app_settings
        app_settings = DjangoAWSS3StorageSettings()
