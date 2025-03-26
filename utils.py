from datetime import date
from pathlib import Path
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

REPORT_SUFFIX = "_stock_report.md"
PATH_TO_WEB_REPORT = "WebStockReportWriter/web_reports/"
PATH_TO_DATA_REPORT = "StockDataReportWriter/data_reports/"


def save_markdown_to_file(markdown_string, stock_symbol, report_type) -> str:
    logging.info(f"************************save_markdown_to_file for: {markdown_string}")
    """
    Save a given markdown string to a file on local disk.

    :param markdown_string: String containing markdown content.
    :param stock_symbol: The stock which info are being stored.
    """
    OUTCOME_MESSAGE = "Report successfully generated and stored"
    try:
        # Path configuration
        MD_OUTPUT_DIR = Path(f'{report_type}_reports/{stock_symbol}')
        MD_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        # Get today's date and format PDF name
        today = date.today().strftime("%Y%m%d")
        report_name = f"{today}_stock_report.md"

        report_path = MD_OUTPUT_DIR / report_name
        # Open the file in write mode ('w')
        with open(report_path, 'w', encoding='utf-8') as file:
            # Write the markdown content to the file
            file.write(markdown_string)
        logging.info(f"Markdown content saved to {report_path}")

    except IOError as e:
        logging.error(f"************************An error occurred while writing to file: {e}")
        OUTCOME_MESSAGE = "An Error has occurred: Unable to store the report"
    return OUTCOME_MESSAGE


def combine_markdown_files(file1_path, file2_path):
    """
    Reads and combines the contents of two Markdown files.

    :param file1_path: Path to the first Markdown file.
    :param file2_path: Path to the second Markdown file.
    :return: A string containing the combined contents of both input Markdown files.
    """
    try:
        # Open and read the contents of the first file
        with open(file1_path, 'r', encoding='utf-8') as file1:
            content1 = file1.read()
        # Open and read the contents of the second file
        with open(file2_path, 'r', encoding='utf-8') as file2:
            content2 = file2.read()

        # Combine the contents of both files
        combined_content = content1 + "\n\n" + content2
        logging.info(f"combine_markdown_files: combined content output: {combined_content}")
        return combined_content
    except FileNotFoundError as fe:
        logging.error(f"************************An error occurred while writing to file: {fe}")
        return f"Error: One or both of the files at paths '{file1_path}' and '{file2_path}' were not found."
    except Exception as e:
        logging.error(f"************************An error occurred while writing to file: {e}")
        return f"An unexpected error occurred: {str(e)}"
