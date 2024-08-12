from pkrhistoryparser.history_parsers.cloud import CloudHandHistoryParser
from pkrhistoryparser.settings import BUCKET_NAME

if __name__ == "__main__":
    parser = CloudHandHistoryParser(BUCKET_NAME)
    parser.parse_new_hand_histories()
