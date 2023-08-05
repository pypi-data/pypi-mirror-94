import os

from setuptools import setup, find_packages


with open('requirements.txt') as reqs_file:
    requirements = reqs_file.readlines()

with open('README.md') as desc_file:
    long_description = desc_file.read()

setup(
    name='django-aws-s3-storage',
    version=os.getenv('BITBUCKET_TAG', '1.0.0rc'),
    description='AWS S3 Bucket file storage system for Django applications',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Gustavo Valentim',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.6',
    install_requires=requirements,
)
