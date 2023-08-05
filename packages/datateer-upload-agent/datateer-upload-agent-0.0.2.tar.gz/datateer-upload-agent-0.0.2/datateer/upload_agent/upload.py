from datetime import date
from pathlib import Path

from botocore.exceptions import ClientError
import boto3
import click

from .config import get_feed, load_config
from .constants import KEY_TEMPLATE

def format_s3_key(feed_key, file_name):
    feed = get_feed(feed_key)
    return KEY_TEMPLATE.format(
        provider=feed['provider'],
        source=feed['source'],
        feed=feed['feed'],
        export_date=date.today().strftime('%Y-%d-%m'),
        file=file_name
    )

def get_resource(config):
    return boto3.resource(
        's3',
        aws_access_key_id=config['upload-agent']['access-key'],
        aws_secret_access_key=config['upload-agent']['access-secret']
    )

def upload(feed_key: str, path: str) -> None:
    path = Path(path)
    key = format_s3_key(feed_key, path.name)
    
    config = load_config()    
    s3 = get_resource(config)

    bucket = config['upload-agent']['raw-bucket']

    click.echo(f'Uploading {str(path.absolute())} to s3://{bucket}/{key}')
    s3.Bucket(bucket).upload_file(str(path.absolute()), key)
    