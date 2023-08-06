import asyncio
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from pathlib import Path
from threading import Thread
from typing import Any, Callable, List
from uuid import uuid4

import aioboto3
from botocore.config import Config
import boto3

from .. import Connection, ConfigS3


#######################################################################################################################
# Utils

def _run_aysnc(func_async: Callable, *args) -> None:
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    event_loop.run_until_complete(func_async(*args))


def _run_threaded_async(func_async: Callable, *args):
    t = Thread(target=_run_aysnc, args=(func_async, *args))
    t.start()
    t.join()


class _S3:
    _client: Any = None

    @classmethod
    def client(cls):
        if cls._client is None:
            cls._client = boto3.session.Session().client('s3', config=Config(max_pool_connections=200))
        return cls._client


_ACL = {'ACL': 'bucket-owner-full-control'}


def _list_keys(bucket: str, key_prefix: str) -> List[str]:
    r = _S3.client().list_objects_v2(Bucket=bucket, Prefix=key_prefix)
    keys = [result['Key'] for result in r['Contents']]
    return keys


#######################################################################################################################

class DataTransfer:
    """
    In a class as static methods, to allow easier monkeypatching in tests
    """
    @staticmethod
    def upload_bytes(upload_config, data: BytesIO) -> str:
        data.seek(0)
        transfer_id = str(uuid4())
        key = f'{upload_config.key_prefix}{transfer_id}/0.data'
        _S3.client().upload_fileobj(Fileobj=data, Bucket=upload_config.bucket_region(), Key=key, ExtraArgs=_ACL)
        return transfer_id

    @staticmethod
    def upload_local_file(upload_config, local_file: str, file_suffix: str) -> None:
        key = f'{upload_config.key_prefix}{file_suffix}'
        _S3.client().upload_file(Bucket=upload_config.bucket_region(), Key=key, Filename=local_file, ExtraArgs=_ACL)

    @staticmethod
    def download_to_bytes(download_config, transfer_id: str) -> BytesIO:
        buf = BytesIO()
        key = f'{download_config.key_prefix}{transfer_id}/0.parquet'
        _S3.client().download_fileobj(Bucket=download_config.bucket_region(), Key=key, Fileobj=buf)
        return buf

    @staticmethod
    def download_to_local_files(download_config, transfer_id: str, path: str, is_folder: bool) -> None:
        bucket = download_config.bucket_region()
        key_prefix = f'{download_config.key_prefix}{transfer_id}/'
        keys = _list_keys(bucket, key_prefix)
        if is_folder:
            for num, key in enumerate(keys):
                _S3.client().download_file(Bucket=bucket, Key=key, Filename=path.format(num))
        else:
            _S3.client().download_file(Bucket=bucket, Key=keys[0], Filename=path)


#######################################################################################################################
# Uploads

def upload_local_files(path: str, transfer_id: str) -> None:
    # TODO: check if it needs to be a dir or can be a prefix?
    path = Path(path)
    paths = [str(path)] if path.is_file() else [str(path_) for path_ in sorted(path.iterdir())]
    for file_num in range(len(paths)):
        DataTransfer.upload_local_file(Connection.session.upload_config, paths[file_num],
                                       f'{transfer_id}/{file_num}.data')


# async def _copy_s3_to_s3_async(source_bucket: str, source_keys: List[str],
#                                dest_bucket: str, dest_key_prefix: str) -> None:
#     async with aioboto3.client('s3', config=ConfigS3.config()) as s3:
#         await asyncio.gather(*[ xxx for key_num in range(len(source_keys))])


def _copy_s3_to_s3(args):
    # noinspection PyUnresolvedReferences
    config = boto3.s3.transfer.TransferConfig(max_concurrency=200)
    _S3.client().copy(
        CopySource={'Bucket': args[0], 'Key': args[1]}, Bucket=args[2], Key=args[3], Config=config,
        ExtraArgs={'ACL': 'bucket-owner-full-control'}
        # SSECustomerAlgorithm='AES256',
    )


def upload_s3_files(path: str, transfer_id: str) -> str:
    """
    Problems:
    - boto3 and s3fs don't have a native recursive (parallelized) copy, and as such are too slow
    Solution:
    - async + aioboto3 for speed, though needs a wrapper thread to not mess with caller async status
    """
    bucket, key_prefix = path[5:].split('/', 1)
    aws_region = _S3.client().get_bucket_location(Bucket=bucket)['LocationConstraint']
    keys_to_upload = _list_keys(bucket, key_prefix)
    upload_config = Connection.session.upload_config
    transfers = [(bucket, key, upload_config.bucket_region(aws_region), f'{upload_config.key_prefix}{transfer_id}/{key_num}.parquet')
                 for key_num, key in enumerate(keys_to_upload)]
    with ThreadPoolExecutor(max_workers=20) as executor:
        list(executor.map(_copy_s3_to_s3, transfers))  # list is necessary as map returns a generator
    # _run_threaded_async(_copy_s3_to_s3_async, bucket, source_keys,
    #                     Connection.session.upload_config.bucket, dest_key_prefix)
    return aws_region


#######################################################################################################################
# Downloads


async def _download_to_s3_async(terality_bucket: str, terality_keys: List[str],
                                client_bucket: str, client_key_prefix: str) -> None:
    async with aioboto3.session.Session().client('s3', config=ConfigS3.config()) as s3:
        await asyncio.gather(*[
            s3.copy_object(
                CopySource={'Bucket': terality_bucket, 'Key': terality_key},
                Bucket=client_bucket, Key=client_key_prefix.format(key_num),
                # SSECustomerAlgorithm='AES256',
            )
            for key_num, terality_key in enumerate(terality_keys)
        ])


def download_to_s3_files(transfer_id: str, aws_region: str, destination_s3_path: str) -> None:
    download_config = Connection.session.download_config
    bucket = download_config.bucket_region(aws_region)
    terality_keys = _list_keys(bucket, f'{download_config.key_prefix}{transfer_id}/')
    client_bucket, client_key_prefix = destination_s3_path[5:].split('/', 1)
    _run_threaded_async(_download_to_s3_async, bucket, terality_keys, client_bucket, client_key_prefix)
