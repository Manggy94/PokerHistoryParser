import os
from .abstract import AbstractSummaryParser


class LocalSummaryParser(AbstractSummaryParser):

    def __init__(self, data_dir: str):
        data_dir = self.correct_data_dir(data_dir)
        self.raw_dir = os.path.join(data_dir, "summaries", "raw")
        self.parsed_dir = os.path.join(data_dir, "summaries", "parsed")

    @staticmethod
    def correct_data_dir(data_dir: str) -> str:
        if not os.path.exists(data_dir):
            data_dir = data_dir.replace("C:/", "/mnt/c/")
        return data_dir

    def list_summary_keys(self) -> list:
        summaries_list = [os.path.join(root, file)
                          for root, _, files in os.walk(self.raw_dir)
                          for file in files if file.endswith(".txt")]
        return summaries_list

    def get_text(self, file_key: str) -> str:
        with open(file_key, "r", encoding="utf-8") as file:
            content = file.read()
        return content

    def check_is_parsed(self, summary_key: str) -> bool:
        parsed_key = self.get_parsed_key(summary_key)
        return os.path.exists(parsed_key)

    def save_parsed_summary(self, summary_key: str, json_summary: str) -> None:
        parsed_key = self.get_parsed_key(summary_key)
        os.makedirs(os.path.dirname(parsed_key), exist_ok=True)
        with open(parsed_key, "w", encoding="utf-8") as file:
            file.write(json_summary)
