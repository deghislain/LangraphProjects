from datetime import date
from pathlib import Path

from utils import combine_markdown_files, REPORT_SUFFIX, PATH_TO_WEB_REPORT, PATH_TO_DATA_REPORT


def perform_financial_analyse(stock_symbol: str) -> str:
    import os

    # Get the current working directory
    current_directory = os.getcwd()

    # Print the current directory
    print(f"Current working directory: {current_directory}")
    report_name = stock_symbol + "/" + date.today().strftime("%Y%m%d") + REPORT_SUFFIX
    web_path = Path(PATH_TO_WEB_REPORT + report_name)
    data_path = Path(PATH_TO_DATA_REPORT + report_name)
    combined_report = combine_markdown_files(web_path, data_path)
    return combined_report


def main(stock_symbol: str):
    return perform_financial_analyse(stock_symbol)


if __name__ == "__main__":
    response = main("IBM")
    print(response)
