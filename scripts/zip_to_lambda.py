import os

from scripts.utils import make_lambda_function, create_zip_archive

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKAGE_NAME = "pkrhistoryparser"
SOURCE_DIR = os.path.join(BASE_DIR, PACKAGE_NAME)
DIST_DIR = os.path.join(BASE_DIR, "dist")
HISTORY_PARSER_HANDLER = f"{PACKAGE_NAME}.lambda.history_parser.lambda_handler"
SUMMARY_PARSER_HANDLER = f"{PACKAGE_NAME}.lambda.summary_parser.lambda_handler"
HISTORY_FUNCTION_NAME = "history_parser"
SUMMARY_FUNCTION_NAME = "summary_parser"
FUNCTION_ROLE = "LambdaS3FilesManager"
RUNTIME = "python3.12"
ARCHIVE_NAME = f"{PACKAGE_NAME}.zip"
HISTORY_ARCHIVE_PATH = os.path.join(DIST_DIR, ARCHIVE_NAME)
SUMMARY_ARCHIVE_PATH = os.path.join(DIST_DIR, ARCHIVE_NAME)


def make_history_parser():
    """
    Creates a lambda function
    """
    create_zip_archive(source_dir=SOURCE_DIR, dist_dir=DIST_DIR, archive_name=ARCHIVE_NAME,
                       archive_path=HISTORY_ARCHIVE_PATH, package_name=PACKAGE_NAME)
    make_lambda_function(function_name=HISTORY_FUNCTION_NAME, archive_path=HISTORY_ARCHIVE_PATH,
                         runtime=RUNTIME, lambda_handler=HISTORY_PARSER_HANDLER,
                         function_role=FUNCTION_ROLE)


def make_summary_parser():
    """
    Creates a lambda function
    """
    create_zip_archive(source_dir=SOURCE_DIR, dist_dir=DIST_DIR, archive_name=ARCHIVE_NAME,
                       archive_path=SUMMARY_ARCHIVE_PATH, package_name=PACKAGE_NAME)
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


