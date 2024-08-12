import boto3
from pkrhistoryparser.summary_parsers.abstract import AbstractSummaryParser


class CloudSummaryParser(AbstractSummaryParser):
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.s3 = boto3.client("s3")
        self.raw_prefix = "data/summaries/raw"
        self.parsed_prefix = "data/summaries/parsed"

    def list_summary_keys(self) -> list:
        paginator = self.s3.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=self.bucket_name, Prefix=self.raw_prefix)
        keys = [obj["Key"] for page in pages for obj in page.get("Contents", [])]
        return keys

    def get_text(self, file_key: str) -> str:
        response = self.s3.get_object(Bucket=self.bucket_name, Key=file_key)
        content = response["Body"].read().decode("utf-8")
        return content

    def check_is_parsed(self, summary_key: str) -> bool:
        parsed_key = self.get_parsed_key(summary_key)
        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=parsed_key)
        return "Contents" in response

    def save_parsed_summary(self, summary_key: str, json_summary: str) -> None:
        parsed_key = self.get_parsed_key(summary_key)
        self.s3.put_object(Bucket=self.bucket_name, Key=parsed_key, Body=json_summary)
