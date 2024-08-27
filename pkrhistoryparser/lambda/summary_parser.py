import json
from pkrhistoryparser.summary_parsers.cloud import CloudSummaryParser


def lambda_handler(event, context):
    for record in event['Records']:
        body = record['body']
        body_dict = json.loads(body)
        message = body_dict["Message"]
        message_dict = json.loads(message)
        message_record = message_dict["Records"][0]
        bucket_name = message_record['s3']['bucket']['name']
        key = message_record['s3']['object']['key']
        print(f"Parsing file {key}")
        try:
            parser = CloudSummaryParser(bucket_name)
            parser.parse_summary(key)
            return {
                'statusCode': 200,
                'body': f'File {key} processed successfully as parsed hand to {parser.get_parsed_key(key)}'
            }
        except Exception as e:
            print(f"Error in lambda_handler: {e}")
            return {
                'statusCode': 500,
                'body': f'Error processing file {key}: {e}'
            }
