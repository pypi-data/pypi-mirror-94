import logging
import pathlib
import tarfile
from urllib.parse import urlparse

import boto3
from botocore.exceptions import ClientError  # type: ignore
from mypy_boto3_s3.client import S3Client


def compress(src: pathlib.Path, name: str) -> str:
    here = pathlib.Path()
    dist = here.resolve() / "data" / "backup" / f"{name}.tar"
    if not dist.exists():
        dist.parent.mkdir()
    with tarfile.open(dist, "w") as f:
        f.add(here / src / "blobstorage", arcname="blobstorage")
        f.add(here / src / "filestorage", arcname="filestorage")
    print(f"Compressed at {dist}")
    return str(dist)


def upload(tar_path: pathlib.Path, s3_uri: str):
    uri = urlparse(s3_uri)
    filename = pathlib.Path(tar_path).resolve().name
    s3_path = uri.path.lstrip("/")

    client: S3Client = boto3.client("s3")
    try:
        with open(tar_path, mode="rb") as f:
            client.upload_fileobj(f, Bucket=uri.netloc, Key=s3_path + filename)
            client.upload_fileobj(f, Bucket=uri.netloc, Key=s3_path + "latest.tar")
            print(f"Succeed upload to {s3_uri.rstrip('/')}/{filename}")
    except ClientError as e:
        logging.error(e)
