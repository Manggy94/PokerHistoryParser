import os

DATA_DIR = os.environ.get("POKER_DATA_DIR")
HISTORIES_DIR = os.path.join(DATA_DIR, "histories")
SUMMARIES_DIR = os.path.join(DATA_DIR, "summaries")
SPLIT_HISTORIES_DIR = os.path.join(HISTORIES_DIR, "split")
PARSED_HISTORIES_DIR = os.path.join(HISTORIES_DIR, "parsed")
BUCKET_NAME = os.environ.get("POKER_AWS_BUCKET_NAME")
TEST_DATA_DIR = os.environ.get("POKER_TEST_DATA_DIR")

if __name__ == "__main__":
    print(DATA_DIR)
    print(BUCKET_NAME)
    print(TEST_DATA_DIR)


