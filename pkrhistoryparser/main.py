import os
from pkrhistoryparser.directories import SPLIT_HISTORIES_DIR, PARSED_HISTORIES_DIR, SUMMARIES_DIR
from pkrhistoryparser.parser import HandHistoryParser

if not os.path.exists(SPLIT_HISTORIES_DIR):
    SPLIT_HISTORIES_DIR = SPLIT_HISTORIES_DIR.replace("C:/", "/mnt/c/")
if not os.path.exists(SUMMARIES_DIR):
    SUMMARIES_DIR.replace("C:/", "/mnt/c/")
if not os.path.exists(PARSED_HISTORIES_DIR):
    PARSED_HISTORIES_DIR.replace("C:/", "/mnt/c/")



if __name__ == "__main__":
    parser = HandHistoryParser(
        split_dir=SPLIT_HISTORIES_DIR,
        parsed_dir=PARSED_HISTORIES_DIR,
        summaries_dir=SUMMARIES_DIR)
    parser.parse_all(check_exists=True)




