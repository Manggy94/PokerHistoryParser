import boto3
import os
import zipfile

from scripts.utils import make_lambda_function, create_zip_archive

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(BASE_DIR, "pkrhistoryparser")
DIST_DIR = os.path.join(BASE_DIR, "dist")
HISTORY_PARSER_HANDLER = "lambda.history_parser.lambda_handler"
SUMMARY_PARSER_HANDLER = "lambda.summary_parser.lambda_handler"
HISTORY_FUNCTION_NAME = "history_parser"
SUMMARY_FUNCTION_NAME = "summary_parser"
FUNCTION_ROLE = "LambdaS3FilesManager"
RUNTIME = "python3.12"
HISTORY_ARCHIVE_NAME = f"{HISTORY_FUNCTION_NAME}.zip"
SUMMARY_ARCHIVE_NAME = f"{SUMMARY_FUNCTION_NAME}.zip"
HISTORY_ARCHIVE_PATH = os.path.join(DIST_DIR, HISTORY_ARCHIVE_NAME)
SUMMARY_ARCHIVE_PATH = os.path.join(DIST_DIR, SUMMARY_ARCHIVE_NAME)


def make_history_parser():
    """
    Creates a lambda function
    """
    create_zip_archive(source_dir=SOURCE_DIR, dist_dir=DIST_DIR, archive_name=HISTORY_ARCHIVE_NAME,
                       archive_path=HISTORY_ARCHIVE_PATH)
    make_lambda_function(function_name=HISTORY_FUNCTION_NAME, archive_path=HISTORY_ARCHIVE_PATH,
                         runtime=RUNTIME, lambda_handler=HISTORY_PARSER_HANDLER,
                         function_role=FUNCTION_ROLE)


def make_summary_parser():
    """
    Creates a lambda function
    """
    create_zip_archive(source_dir=SOURCE_DIR, dist_dir=DIST_DIR, archive_name=SUMMARY_ARCHIVE_NAME,
                       archive_path=SUMMARY_ARCHIVE_PATH)
    make_lambda_function(function_name=SUMMARY_FUNCTION_NAME, archive_path=SUMMARY_ARCHIVE_PATH,
                         runtime=RUNTIME, lambda_handler=SUMMARY_PARSER_HANDLER,
                         function_role=FUNCTION_ROLE)


def zip_and_upload():
    """
    Zips and uploads the lambda functions
    """
    make_history_parser()
    make_summary_parser()


if __name__ == "__main__":
    zip_and_upload()


