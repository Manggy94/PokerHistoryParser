"""This module tests the time needed to parse a split history file or a summary file in local."""

import time
from pkrhistoryparser.settings import DATA_DIR
from pkrhistoryparser.history_parsers.local import LocalHandHistoryParser
from pkrhistoryparser.summary_parsers.local import LocalSummaryParser


def speed_parse_hand_history():
    """Test the time needed to parse a split history file in local."""
    parser = LocalHandHistoryParser(DATA_DIR)
    last_10_files = parser.list_split_histories_keys()[-10:]
    start = time.time()
    for _ in range(10):
        for file_key in last_10_files:
            parser.parse_hand_history(file_key)
    end = time.time()
    total_time = end - start
    average_time = total_time / 100
    print(f"Total time to parse 100 split history files: {total_time:.2f} seconds")
    print(f"Average time to parse a split history file: {average_time:.4f} seconds or "
          f"{average_time * 1000:.1f} milliseconds")


def speed_parse_summary():
    """Test the time needed to parse a summary file in local."""
    parser = LocalSummaryParser(DATA_DIR)
    last_10_files = parser.list_summary_keys()[-10:]
    start = time.time()
    for _ in range(10):
        for file_key in last_10_files:
            parser.parse_summary(file_key)
    end = time.time()
    total_time = end - start
    average_time = total_time / 100
    print(f"Total time to parse 100 summary files: {total_time:.2f} seconds")
    print(f"Average time to parse a summary file: {average_time:.4f} seconds or "
          f"{average_time * 1000:.1f} milliseconds")


if __name__ == "__main__":
    speed_parse_hand_history()
    speed_parse_summary()