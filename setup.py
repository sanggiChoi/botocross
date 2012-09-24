#!/usr/bin/python
from distutils.core import setup
from setuptools import find_packages

setup(name='botocross',
      version='1.0.1',
      packages=find_packages(),
      scripts=[
        'authorize-securitygroups.py',
        'create-buckets.py',
        'create-images.py',
        'create-securitygroups.py',
        'create-snapshots.py',
        'create-stacks.py',
        'create-topics.py',
        'decode-logs.py',
        'delete-buckets.py',
        'delete-images.py',
        'delete-keypairs.py',
        'delete-keys.py',
        'delete-securitygroups.py',
        'delete-snapshots.py',
        'delete-stacks.py',
        'delete-topics.py',
        'describe-images.py',
        'describe-instances.py',
        'describe-regions.py',
        'describe-securitygroups.py',
        'describe-snapshots.py',
        'describe-stacks.py',
        'describe-tags.py',
        'describe-volumes.py',
        'import-keypairs.py',
        'read-buckets.py',
        'revoke-securitygroups.py',
        'subscribe-topics.py',
        'update-stacks.py',
        'upload-keys.py',
        'validate-credentials.py',
        'validate-template.py',
      ],
      license='LICENSE',
      install_requires=[
        "boto >= 2.5.2",
      ],
      )
