import logging
import pathlib
import tarfile
import tempfile
from urllib.parse import urlparse

import boto3
from botocore.exceptions import ClientError  # type: ignore
from mypy_boto3_s3.client import S3Client


def download(s3_uri: str) -> pathlib.Path:
    uri = urlparse(s3_uri)
    tar_path = pathlib.Path(uri.path.lstrip("/"))

    client: S3Client = boto3.client("s3")
    dist = pathlib.Path(tempfile.gettempdir()) / "plone-data" / tar_path.name
    try:
        with open(dist, mode="wb") as f:
            client.download_fileobj(Bucket=uri.netloc, Key=str(tar_path), Fileobj=f)
    except ClientError as e:
        logging.error(e)
    return dist


def extract(src: pathlib.Path, dist: pathlib.Path):
    with tarfile.open(src, "r") as f:
        f.extractall(dist)
