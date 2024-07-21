from s3_parser import S3HandHistoryParser
from directories import BUCKET_NAME

if __name__ == "__main__":
    parser = S3HandHistoryParser(bucket_name=BUCKET_NAME)
    print(f"Parser has been correctly initialized.")
    keys = parser.list_histories_keys()
    print(f"Number of files: {len(keys)}")
    first_file = keys[0]

    print(f"First file: {first_file}")
    destination_key = parser.get_destination_path(first_file)
    print(f"Destination path: {destination_key}")
    summary_path = parser.get_summary_path(first_file)
    print(f"Summary path: {summary_path}")
    parser.parse_to_json(first_file)