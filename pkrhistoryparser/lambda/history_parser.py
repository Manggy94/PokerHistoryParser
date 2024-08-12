from pkrhistoryparser.history_parsers.cloud import CloudHandHistoryParser


def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    print(f"Splitting file {key}")
    try:
        parser = CloudHandHistoryParser(bucket_name)
        parser.parse_hand_history(key)
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
