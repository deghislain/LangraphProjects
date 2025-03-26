from datetime import date
from pathlib import Path
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def save_markdown_to_file(markdown_string, stock_symbol, report_type)-> str:
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
