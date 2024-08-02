from pkrhistoryparser.summary_parsers.local import LocalSummaryParser
from pkrhistoryparser.settings import DATA_DIR


if __name__ == "__main__":
    parser = LocalSummaryParser(DATA_DIR)
    parser.parse_summaries()
