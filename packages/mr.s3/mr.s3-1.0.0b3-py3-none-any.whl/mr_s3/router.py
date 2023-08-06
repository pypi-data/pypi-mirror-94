from datetime import datetime
import logging
import os
import pathlib

import click

from plone_sync_s3.push import compress, upload
from plone_sync_s3.pull import download, extract


@click.group()
def cli():
    if os.getenv("DEBUG") is not None:
        logging.basicConfig(level="DEBUG")


@cli.command(help="Compress blobstorage and filestorage and upload to s3")
@click.argument("src", type=click.Path(exists=True))
@click.argument("s3_uri", type=str)
@click.option(
    "-n",
    "--filename",
    default=datetime.now().strftime("%Y%m%d-%H%M%S"),
)
def push(src: pathlib.Path, s3_uri: str, filename: str):
    tar_path = compress(src, filename)
    upload(tar_path, s3_uri)


@cli.command(help="Download tar file and extract")
@click.argument("s3_uri", type=str)
@click.argument("dist", type=click.Path())
def pull(s3_uri, dist: pathlib.Path):
    tarfile = download(s3_uri)
    extract(tarfile, dist)
    print(f"Finished. result file: {dist}")


if __name__ == "__main__":
    cli()
