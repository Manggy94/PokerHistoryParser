import os
from .abstract import AbstractHandHistoryParser


class LocalHandHistoryParser(AbstractHandHistoryParser):

    def __init__(self, data_dir: str):
        self.data_dir = self.correct_data_dir(data_dir)
        self.split_dir = os.path.join(self.data_dir, "histories", "split")
        self.parsed_dir = os.path.join(self.data_dir, "histories", "parsed")
        self.correction_split_keys_file_key = os.path.join(self.data_dir, "correction_split_keys.txt")
        self.correction_parsed_keys_file_key = os.path.join(self.data_dir, "correction_parsed_keys.txt")

    @staticmethod
    def correct_data_dir(data_dir: str) -> str:
        if not os.path.exists(data_dir):
            data_dir = data_dir.replace("C:/", "/mnt/c/")
        return data_dir

    def list_split_histories_keys(self, directory_key: str = None) -> list:
        directory = directory_key or self.split_dir
        split_keys = [
            os.path.join(root, filename)
            for root, _, filenames in os.walk(directory)
            for filename in filenames if filename.endswith('.txt')
        ]
        return split_keys

    def get_text(self, key: str) -> str:
        with open(key, 'r', encoding='utf-8') as file:
            content = file.read()
        return content

    def write_text(self, key: str, content: str) -> None:
        with open(key, 'w', encoding='utf-8') as file:
            file.write(content)

    def write_text_from_list(self, key: str, content: list) -> None:
        with open(key, 'w', encoding='utf-8') as file:
            for line in content:
                file.write(line + "\n")

    def check_is_parsed(self, split_key: str) -> bool:
        parsed_key = self.get_parsed_key(split_key)
        return os.path.exists(parsed_key)

    def save_parsed_hand(self, split_key: str, json_hand: str) -> None:
        parsed_key = self.get_parsed_key(split_key)
        os.makedirs(os.path.dirname(parsed_key), exist_ok=True)
        with open(parsed_key, 'w', encoding='utf-8') as file:
            file.write(json_hand)



