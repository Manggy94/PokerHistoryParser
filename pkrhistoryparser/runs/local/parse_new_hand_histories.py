from pkrhistoryparser.history_parsers.local import LocalHandHistoryParser
from pkrhistoryparser.settings import DATA_DIR

if __name__ == "__main__":
    parser = LocalHandHistoryParser(DATA_DIR)
    parser.parse_new_hand_histories()
