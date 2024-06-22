import os
from dotenv import load_dotenv
load_dotenv()

SOURCE_DIR = os.environ.get("SOURCE_DIR")
HISTORIES_DIR = os.path.join(SOURCE_DIR, "histories")
SUMMARIES_DIR = os.path.join(SOURCE_DIR, "summaries")
SPLIT_HISTORIES_DIR = os.path.join(HISTORIES_DIR, "split")
PARSED_HISTORIES_DIR = os.path.join(HISTORIES_DIR, "parsed")


