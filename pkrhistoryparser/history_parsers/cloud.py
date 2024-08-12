import boto3
from .abstract import AbstractHandHistoryParser


class CloudHandHistoryParser(AbstractHandHistoryParser):

    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.s3 = boto3.client("s3")
        self.split_prefix = "data/histories/split"
        self.parsed_prefix = "data/histories/parsed"

    def list_split_histories_keys(self) -> list:
        paginator = self.s3.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=self.bucket_name, Prefix=self.split_prefix)
        keys = [obj["Key"] for page in pages for obj in page.get("Contents", [])]
        return keys

    def get_text(self, key: str) -> str:
        response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
        content = response["Body"].read().decode("utf-8")
        return content

    def check_is_parsed(self, split_key: str) -> bool:
        parsed_key = self.get_parsed_key(split_key)
        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=parsed_key)
        return "Contents" in response

    def save_parsed_hand(self, split_key: str, json_hand: str) -> None:
        parsed_key = self.get_parsed_key(split_key)
        self.s3.put_object(Bucket=self.bucket_name, Key=parsed_key, Body=json_hand)


