from pkrhistoryparser.parsers.s3 import S3HandHistoryParser
from pkrhistoryparser.settings import BUCKET_NAME

if __name__ == "__main__":
    parser = S3HandHistoryParser(BUCKET_NAME)
    parser.parse_hand_histories()