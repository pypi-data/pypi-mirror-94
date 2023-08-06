mr.s3
=====

Syncing scripts Plone data between local and AWS S3

Installation
------------

Just run ``pip install mr.s3``

Uses
----

You have to set AWS Credentials to ``$HOME/.aws/credentials``.

See also Boto3's docs. https://github.com/boto/boto3#using-boto3


::

$ mr.s3 push path/to/datadir  # uploading
$ mr.s3 pull path/to/datadir  # downloading

Features
--------

- Compress blobstorage and filestorage as tar, and upload to S3
- Download them from S3, and extract to specific directory

Dependences
-----------

- boto3 https://github.com/boto/boto3
- click https://github.com/pallets/click

