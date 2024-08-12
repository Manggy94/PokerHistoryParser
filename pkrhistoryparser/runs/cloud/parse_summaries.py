from pkrhistoryparser.summary_parsers.cloud import CloudSummaryParser
from pkrhistoryparser.settings import BUCKET_NAME

if __name__ == "__main__":
    parser = CloudSummaryParser(BUCKET_NAME)
    parser.parse_summaries()
