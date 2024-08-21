import boto3
from .abstract import AbstractHandHistoryParser


class CloudHandHistoryParser(AbstractHandHistoryParser):

    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.s3 = boto3.client("s3")
        self.data_dir = "data"
        self.split_dir = "data/histories/split"
        self.parsed_dir = "data/histories/parsed"
        self.correction_split_keys_file_key = "data/correction_split_keys.txt"
        self.correction_parsed_keys_file_key = "data/correction_parsed_keys.txt"

    def list_split_histories_keys(self, directory_key: str = None) -> list:
        paginator = self.s3.get_paginator("list_objects_v2")
        directory = directory_key or self.split_dir
        pages = paginator.paginate(Bucket=self.bucket_name, Prefix=directory)
        keys = [obj["Key"] for page in pages for obj in page.get("Contents", [])]
        return keys

    def get_text(self, key: str) -> str:
        response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
        content = response["Body"].read().decode("utf-8")
        return content

    def write_text(self, key: str, content: str) -> None:
        self.s3.put_object(Bucket=self.bucket_name, Key=key, Body=content)

    def write_text_from_list(self, key: str, content: list) -> None:
        content = "\n".join(content)
        self.s3.put_object(Bucket=self.bucket_name, Key=key, Body=content)

    def check_is_parsed(self, split_key: str) -> bool:
        parsed_key = self.get_parsed_key(split_key)
        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=parsed_key)
        return "Contents" in response

    def save_parsed_hand(self, split_key: str, json_hand: str) -> None:
        parsed_key = self.get_parsed_key(split_key)
        self.s3.put_object(Bucket=self.bucket_name, Key=parsed_key, Body=json_hand)


