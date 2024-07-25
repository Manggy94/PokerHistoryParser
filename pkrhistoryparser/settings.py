import os
from dotenv import load_dotenv
load_dotenv()

DATA_DIR = os.environ.get("DATA_DIR")
HISTORIES_DIR = os.path.join(DATA_DIR, "histories")
SUMMARIES_DIR = os.path.join(DATA_DIR, "summaries")
SPLIT_HISTORIES_DIR = os.path.join(HISTORIES_DIR, "split")
PARSED_HISTORIES_DIR = os.path.join(HISTORIES_DIR, "parsed")
BUCKET_NAME = os.environ.get("BUCKET_NAME")

if __name__ == "__main__":
    print(DATA_DIR)


