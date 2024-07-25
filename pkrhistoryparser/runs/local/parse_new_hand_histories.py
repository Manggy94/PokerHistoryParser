from pkrhistoryparser.parsers.local import LocalHandHistoryParser
from pkrhistoryparser.settings import BUCKET_NAME

if __name__ == "__main__":
    parser = LocalHandHistoryParser(BUCKET_NAME)
    parser.parse_new_hand_histories()
